"""Local cue performance, deterministic Foley and an original ducked score."""
import hashlib
import json
import math
from pathlib import Path
import re
import wave
import numpy as np

RATE = 24000
PROFILES = {'normal':(1.07,1.),'deadpan':(.96,.92),'whispering':(.92,.65),
            'panicked':(1.20,1.05),'excited':(1.15,1.05),'laughing':(1.09,.96),
            'shouting':(1.11,1.12),'sighing':(.94,.87),'gasp':(1.06,1.)}
TAGS = set(PROFILES) | {'pause','beat'}
SFX = {'thump','ping','stamp','swish','glitch','crunch','none'}
ROOT = Path(__file__).resolve().parents[1]

def parse(line):
    result = []
    style = 'normal'
    for part in re.split(r'(\[[^\[\]]+\])', line):
        if part.startswith('[') and part.endswith(']'):
            tag = part[1:-1].strip().lower()
            if tag not in TAGS:
                raise ValueError(f'Unknown performance tag {part}')
            if tag in ('pause','beat','laughing','gasp','sighing'):
                result.append(('fx',tag,style))
            if tag in PROFILES:
                style = tag
        elif part.strip():
            if '[' in part or ']' in part:
                raise ValueError('Malformed performance tag: '+part)
            result.append(('speech',part.strip(),style))
    return result

def wav(path, samples):
    with wave.open(str(path),'wb') as out:
        out.setparams((1,2,RATE,0,'NONE','not compressed'))
        out.writeframes((np.clip(samples,-1,1)*32767).astype('<i2').tobytes())

def envelope(audio):
    if len(audio):
        n=min(120,len(audio)//2)
        if n:
            ramp=np.linspace(0,1,n);audio[:n]*=ramp;audio[-n:]*=ramp[::-1]
    return audio

class Voice:
    def __init__(self, models):
        import onnxruntime as ort
        from kokoro_onnx import Kokoro
        options=ort.SessionOptions()
        options.intra_op_num_threads=2
        options.inter_op_num_threads=1
        session=ort.InferenceSession(str(models/'kokoro-v1.0.int8.onnx'),options,
                                     providers=['CPUExecutionProvider'])
        self.engine=Kokoro.from_session(session,str(models/'voices-v1.0.bin'))
    def say(self, text, voice, style, lang):
        speed, gain = PROFILES[style]
        data, rate=self.engine.create(text,voice=voice,speed=speed,lang=lang)
        if rate!=RATE: raise ValueError(f'Unexpected sample rate {rate}')
        data=np.asarray(data,dtype=np.float32).copy()
        if style=='whispering':
            # Blend a quiet breath-shaped layer with consonants for intelligibility.
            rng=np.random.default_rng(204)
            data=.74*data + .26*np.abs(data)*rng.standard_normal(len(data))
        if style=='shouting':
            data=np.tanh(data*1.55)/1.23
        return envelope(data*gain)

def breath(tag):
    if tag in ('pause','beat'):
        return np.zeros(round(RATE*(.30 if tag=='pause' else .15)))
    length=.19 if tag=='gasp' else .38
    t=np.arange(round(RATE*length))/RATE
    noise=np.random.default_rng(901).standard_normal(len(t))
    env=np.sin(np.pi*t/length)**2
    return .08*env*np.convolve(noise,np.ones(5)/5,mode='same')

def effect(name):
    length={'thump':.21,'ping':.35,'stamp':.16,'swish':.24,'glitch':.2,'crunch':.27}.get(name,0)
    t=np.arange(round(RATE*length))/RATE
    if not len(t):return t
    rng=np.random.default_rng(43)
    if name=='ping': y=np.sin(2*np.pi*990*t)+.35*np.sin(2*np.pi*1485*t)
    elif name=='swish': y=rng.normal(0,.5,len(t))*np.sin(np.pi*t/length)**2
    elif name=='glitch': y=np.sign(np.sin(2*np.pi*(240*t+800*t*t)))*(.4+.6*np.cos(50*t)**2)
    elif name=='crunch': y=rng.normal(0,.65,len(t))*np.cos(52*t)**8
    else: y=np.sin(2*np.pi*(120*t-180*t*t)) + (.6 if name=='stamp' else .10)*rng.normal(0,.55,len(t))
    return envelope(.18*y*np.exp(-t/(length/3)))

def soundtrack(plan, work, models, cache):
    cast={c['id']:c for c in plan['cast']}
    cache.mkdir(parents=True,exist_ok=True)
    parts=[]; events=[]; captions=[]; samples=0; voice=None
    def add(data):
        nonlocal samples
        parts.append(data);samples+=len(data)
    for si,scene in enumerate(plan['scenes']):
        for bi,beat in enumerate(scene['beats']):
            start=samples
            for kind,value,style in parse(beat['line']):
                at=samples
                if kind=='speech' or value=='laughing':
                    words=value if kind=='speech' else 'Ha, ha!'
                    member=cast[beat['speaker']]
                    settings=[words,member['voice'],member.get('lang','en-us'),style,'v1.2']
                    key=hashlib.sha256(json.dumps(settings).encode()).hexdigest()
                    p=cache/(key+'.npy')
                    if p.exists(): data=np.load(p,allow_pickle=False)
                    else:
                        if voice is None: voice=Voice(models)
                        data=voice.say(words,settings[1],style,settings[2])
                        tmp=p.with_suffix('.tmp.npy');np.save(tmp,data);tmp.replace(p)
                    add(data)
                    if kind=='speech':
                        captions.append({'start':at/RATE,'end':samples/RATE,'text':words})
                else: add(breath(value))
            add(np.zeros(round(RATE*beat.get('hold',.12))))
            events.append({'scene':si,'beat':bi,'id':beat['id'],'start':start/RATE,'end':samples/RATE})
    speech=np.concatenate(parts)
    if not len(speech) or np.max(np.abs(speech))<.015:raise ValueError('Voice track is silent')
    # Preserve expression dynamics, then put dry voice comfortably above music.
    speech=speech*(.75/max(.01,np.max(np.abs(speech))))
    music=np.zeros(len(speech)); foley=music.copy()
    if plan.get('music',True):
        for i,at in enumerate(np.arange(0,len(speech)/RATE,.30)):
            k=round(at*RATE)
            t=np.arange(min(round(RATE*.38),len(speech)-k))/RATE
            hz=[130.81,196,155.56,233.08,130.81,196,174.61,146.83][i%8]
            music[k:k+len(t)]+=.054*np.sin(2*np.pi*hz*t)*np.exp(-10*t)*np.minimum(1,45*t)
        for caption in captions:
            a,b=round(caption['start']*RATE),round(caption['end']*RATE)
            music[a:b]*=.50
    for evt in events:
        beat=plan['scenes'][evt['scene']]['beats'][evt['beat']]
        fx=effect(beat.get('sfx','none'))
        k=round((evt['start']+(evt['end']-evt['start'])*beat.get('hit',0))*RATE)
        n=min(len(fx), len(foley)-k)
        if n>0: foley[k:k+n]+=fx[:n]
    mix=speech+music+foley
    mix*=min(1,.92/max(.01,np.max(np.abs(mix))))
    for name,data in [('voice',speech),('music',music),('foley',foley),('mix',mix)]:
        wav(work/(name+'.wav'),data)
    return events,captions,len(mix)/RATE
