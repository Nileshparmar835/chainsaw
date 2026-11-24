"""Assemble one authored episode. Run from any directory with the project Python."""
import argparse
from bisect import bisect_right
import importlib.util
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import numpy as np
from PIL import Image, ImageDraw
from ink import Canvas, ROOT
from sound import soundtrack, parse, SFX, RATE

FPS=30
def ffmpeg():
    system=shutil.which('ffmpeg')
    if system: return system
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

def doctor():
    import kokoro_onnx
    from ink import font
    from sound import Voice
    font(48)
    subprocess.run([ffmpeg(),'-loglevel','error','-f','lavfi','-i','color=s=16x16:d=0.1',
                    '-f','lavfi','-i','anullsrc','-t','0.1','-c:v','libx264','-c:a','aac','-f','mp4','-movflags','frag_keyframe+empty_moov','-'],
                   stdout=subprocess.DEVNULL,check=True)
    Voice(ROOT/'models')
    print('Ready: local Kokoro, font, H.264 and AAC.')

def validate(plan):
    for k in ('topic','title','route','hook','payoff','cast','scenes'):
        if not plan.get(k):raise ValueError('Missing '+k)
    ids=set()
    for c in plan['cast']:
        for k in ('id','design','role','voice'):
            if not c.get(k):raise ValueError('Missing cast '+k)
        if c['id'] in ids:raise ValueError('Duplicate cast id '+c['id'])
        ids.add(c['id'])
    seen=set()
    for s in plan['scenes']:
        for k in ('setting','camera','elements','action','beats'):
            if not s.get(k):raise ValueError('Missing scene '+k)
        if not set(s.get('cast',[]))<=ids:raise ValueError('Unknown scene cast')
        for b in s['beats']:
            if b['id'] in seen:raise ValueError('Duplicate beat '+b['id'])
            seen.add(b['id'])
            if b['speaker'] not in ids or not b.get('visual') or not parse(b['line']):
                raise ValueError('Missing acting or audio in '+b['id'])
            if b.get('sfx','none') not in SFX or not 0<=b.get('hit',0)<1 or not 0<=b.get('hold',.12)<=2:
                raise ValueError('Invalid sound or timing in '+b['id'])

def stamp(seconds):
    ms=round(seconds*1000);s,ms=divmod(ms,1000);m,s=divmod(s,60);h,m=divmod(m,60)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

def notes(plan,path):
    rows=['# '+plan['title'],'',plan['topic'],'','**Story route** '+plan['route'],
          '','**Hook** '+plan['hook'],'','**Payoff** '+plan['payoff'],'','## Cast','']
    for c in plan['cast']:rows.append(f"- **{c['id']}** — {c['role']}. {c['design']}. Voice `{c['voice']}`.")
    for i,s in enumerate(plan['scenes'],1):
        rows+=['',f"## {i}. {s['setting']}",'','Cast — '+', '.join(s['cast']),
               '','Elements — '+', '.join(s['elements']),'','Camera — '+s['camera'],'',s['action'],'']
        for b in s['beats']:rows.append(f"- **{b['speaker']}** {b['line']}  \n  {b['visual']} · {b.get('sfx','none')}")
    path.write_text('\n'.join(rows)+'\n',encoding='utf-8')

def verify(path,events,width,duration,out):
    cli=ffmpeg()
    run=subprocess.run([cli,'-hide_banner','-i',str(path),'-map','0:v:0','-vf','scale=90:160',
                        '-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True,check=True)
    desc=run.stderr.decode(errors='replace')
    if not re.search(r'Video: h264[^\n]*?'+f'{width}x{width*16//9}'+r'\b[^\n]*?30 fps',desc) or 'Audio: aac' not in desc:
        raise ValueError('Unexpected codec, dimensions or frame rate')
    frames=np.frombuffer(run.stdout,np.uint8).reshape(-1,160,90,3)
    audio=subprocess.check_output([cli,'-v','error','-i',str(path),'-vn','-ar','24000','-ac','1','-f','s16le','-'])
    pcm=np.frombuffer(audio,'<i2').astype(float)/32768
    rms=lambda a:float(np.sqrt(np.mean(a*a))) if len(a) else 0.
    if abs(len(frames)/FPS-duration)>.06 or abs(len(pcm)/RATE-duration)>.13 or rms(pcm)<.01:
        raise ValueError('Decoded audio or video duration/level failed')
    sheet=Image.new('RGB',(4*135,math.ceil(len(events)/4)*260),'#241b2d')
    d=ImageDraw.Draw(sheet);changes={}
    for i,e in enumerate(events):
        start=int(e['start']*FPS);end=max(start+1,int(e['end']*FPS))
        clip=frames[start:end]
        if len(clip)==0:raise ValueError('Missing beat '+e['id'])
        # Exclude subtitle area; record actual movement in rendered artwork.
        region=clip[:,15:115].astype('int16')
        change=float(np.max(np.abs(region-region[0]).mean(axis=(1,2,3))))
        changes[e['id']]=round(change,2)
        if len(clip)>12 and change<.12:raise ValueError('Static artwork in '+e['id'])
        if rms(pcm[round(RATE*e['start']):round(RATE*e['end'])])<.004:
            raise ValueError('Silent beat '+e['id'])
        x,y=i%4*135,i//4*260
        sheet.paste(Image.fromarray(clip[len(clip)//2]).resize((135,240)),(x,y))
        d.text((x+4,y+242),e['id'],fill='white')
    sheet.save(out/'contact-sheet.jpg',quality=88)
    report={'resolution':[width,width*16//9],'fps':FPS,'frames':len(frames),
            'audio_seconds':round(len(pcm)/RATE,3),'video_seconds':round(len(frames)/FPS,3),
            'decoded_audio_rms':round(rms(pcm),4),'decoded_peak':round(float(np.max(np.abs(pcm))),4),
            'motion_per_beat':changes,'review':'Automated decode checks. Inspect timing, acting and sound separately.'}
    (out/'qa.json').write_text(json.dumps(report,indent=2),encoding='utf-8')

def produce(project,out,width,models):
    plan=json.loads((project/'episode.json').read_text(encoding='utf-8'))
    validate(plan);out.mkdir(exist_ok=True,parents=True)
    notes(plan,out/'storyboard.md')
    spec=importlib.util.spec_from_file_location('episode_art',project/'art.py')
    art=importlib.util.module_from_spec(spec);sys.path.insert(0,str(project))
    spec.loader.exec_module(art)
    events,caps,duration=soundtrack(plan,out,models,project/'.cache'/'voice')
    (out/'timeline.json').write_text(json.dumps({'beats':events,'captions':caps},indent=2),encoding='utf-8')
    (out/'captions.srt').write_text('\n\n'.join(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(caps,1))+'\n',encoding='utf-8')
    starts=[e['start'] for e in events];cap_starts=[c['start'] for c in caps]
    scene_start={e['scene']:e['start'] for e in events if e['beat']==0}
    scene_end={e['scene']:e['end'] for e in events}
    with tempfile.TemporaryDirectory(dir=out) as temp:
        target=Path(temp)/'candidate.mp4'
        args=[ffmpeg(),'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{width}x{width*16//9}','-r',str(FPS),'-i','pipe:0','-i',str(out/'mix.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-threads','3','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-af','loudnorm=I=-16:TP=-1.5:LRA=10','-ar','48000','-c:a','aac','-b:a','160k','-movflags','+faststart',str(target)]
        with subprocess.Popen(args,stdin=subprocess.PIPE) as proc:
            try:
                for frame in range(math.ceil(duration*FPS)):
                    t=frame/FPS;e=events[max(0,bisect_right(starts,t)-1)];si=e['scene']
                    beat=plan['scenes'][si]['beats'][e['beat']]
                    q=SimpleNamespace(id=e['id'],scene=si,beat=e['beat'],t=t,local=t-e['start'],
                            u=(t-e['start'])/(e['end']-e['start']),scene_t=t-scene_start[si],
                            scene_u=(t-scene_start[si])/(scene_end[si]-scene_start[si]),direction=beat)
                    canvas=Canvas(width);art.draw(canvas,q)
                    j=bisect_right(cap_starts,t)-1
                    if j>=0 and t<caps[j]['end']:canvas.caption(caps[j]['text'])
                    proc.stdin.write(canvas.image.tobytes())
            finally:proc.stdin.close()
            if proc.wait():raise RuntimeError('Video encode failed')
        verify(target,events,width,duration,out)
        target.replace(out/'final.mp4')
    print(f'{out/"final.mp4"} | {duration:.2f}s | {width}x{width*16//9} | 30 fps')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('project',type=Path,nargs='?')
    p.add_argument('--out',type=Path);p.add_argument('--draft',action='store_true')
    p.add_argument('--doctor',action='store_true');p.add_argument('--models',type=Path,default=ROOT/'models')
    a=p.parse_args()
    if a.doctor:doctor()
    elif a.project:produce(a.project.resolve(),a.out or a.project/('draft' if a.draft else 'output'),360 if a.draft else 1080,a.models)
    else:p.error('Give an episode directory or use --doctor')
