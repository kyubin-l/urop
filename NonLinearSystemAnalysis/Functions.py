import math
import numpy as np
from scipy import signal


def FrameSplit(y, nfft):
    # Split y into overlapping frames with length nfft and 50% overlap
    # Load frames into matrix y_frames with dimensions (nfft, n_tot)
    y_length = len(y)
    n_odd = math.floor(y_length/nfft)
    n_even = math.floor((y_length - nfft/2)/nfft)
    n_tot = n_odd + n_even

    y_frames = np.zeros((nfft, n_tot)) #  Initialize Frame
    
    for i in range(0, n_tot-1):
        i1 = int(i*nfft/2)
        i2 = int(nfft + i*nfft/2)
        y_frames[:,i] = y[i1:i2, ]
    
    return y_frames


def mcoheref(Syy, Sxx, Syx, f):
    
    ninxx = Sxx.shape[0]
    noutyy = Syy.shape[0]
    ninyx = Syx.shape[1]
    noutyx = Syx.shape[0]
    
    if ninxx!=ninyx:
        print('Sxx and Syx must have the same number of inputs')
        return None

    elif noutyy!=noutyx:
        print('Syy and Syx mus thave the same number of outputs')
        return None
    
    nin = ninxx
    nout = noutyy
    
    Gxx = Sxx
    Gyy = Syy
    Gyx = Syx
    
    # Computing determinant of input cross-spectra
    nfreq = len(f)
    detGxx = np.zeros((nfreq, ))
    detGyxx = np.zeros((nfreq, ))
    
    for i in range(nfreq):
        detGxx[i] = np.real(np.linalg.det(np.squeeze(Gxx[:,:,i]).reshape(nin, nin)))
    
    # Multiple coherence
    mCxy = np.zeros((nout, 1, nfreq))
    for i in range(nout):
        # Forming augmented cross-spectrum matrix of the inputs and ouputs for the ith output 
        Gyxx = np.zeros((nin+1, nin+1, nfreq), dtype = 'complex_')
        Gyxx[0,0,:] = Gyy[i,i,:]
        Gyxx[1:,1:,:] = Gxx
        Gyxx[0,1:,:] = Gyx[i,:,:]
        Gyxx[1:,0,:] = np.conj(Gyx[i,:,:])
        
        for k in range(nfreq):
            detGyxx[k] = np.real(np.linalg.det(np.squeeze(Gyxx[:,:,k])))
        
        mCxy[i,:,:] = 1-detGyxx/(np.squeeze(np.real(Gyy[i,i,:]))*detGxx)
        
    return mCxy


def tfest(inputs, outputs, win=None, noverlap=None, nfft=None, Fs=None):
    
    # Input should be an array of Mtimepoints by Nsignals. 
    # Setting default values. Default values are set as set in the scipy.csd function. 
    
    if nfft == None:
        nfft = 256
    
    if Fs == None:
        Fs = 1
    
    if win == None:
        win = np.hanning(nfft)
        
    if noverlap == None:
        noverlap = nfft/2
    
    # si: number of input signals
    # so: number of output signals
    # ti: number of timepoints in
    # to : number of timepoints out    
    
    try:
        si = inputs.shape[1]
    except IndexError:
        si = 1
        inputs = np.reshape(inputs, (len(inputs), 1))
        
    try:
        so = outputs.shape[1]
    except IndexError:
        so = 1
        outputs = np.reshape(outputs, (len(outputs), 1))


    ti = inputs.shape[0]
    to = outputs.shape[0]
    
    sf = int(nfft/2 + 1) #  This depends on if we want to use double sided or one sided. 
    syx = np.zeros((so, si, sf), dtype = 'complex_')
    sxx = np.zeros((si, si, sf), dtype = 'complex_')
    syy = np.zeros((so, so, sf), dtype = 'complex_')
    
    print("Calculating Sxx")
    
    for i in range(si):
        for j in range(i+1):
            f, sxx[i,j,:] = signal.csd(inputs[:,j], inputs[:,i], 
                                       fs=Fs, 
                                       window=np.hanning(nfft), 
                                       noverlap=nfft/2, 
                                       nfft=nfft, 
                                       return_onesided=True, 
                                       scaling='density')
            if i != j:
                sxx[j,i,:] = np.conj(sxx[i,j,:]) 
                
    print("Calculating Syy")
    
    for i in range(so):
        for j in range(i+1):
            f, syy[i,j,:] = signal.csd(outputs[:,j], outputs[:,i], 
                                       fs=Fs, 
                                       window=np.hanning(nfft), 
                                       noverlap=nfft/2, 
                                       nfft=nfft, 
                                       return_onesided=True, 
                                       scaling='density')
            if i != j:
                syy[j,i,:] = np.conj(syy[i,j,:])
    
    
    print("Calculating Syx")
    
    for i in range(so):
        for j in range(si):
            f, syx[i, j, :] = signal.csd(inputs[:,j], outputs[:,i], # Takes conjugate of first value (F) 
                                         fs=Fs, 
                                         window=np.hanning(nfft), 
                                         noverlap=nfft/2, 
                                         nfft=nfft, 
                                         return_onesided=True, 
                                         scaling='density')
            
    print("Calculating transfer function and coherence")
    
    tyx = syx/sxx # look at different definitions of transfer function!
    mcyx = mcoheref(syy, sxx, syx, f)

    return f, tyx, mcyx, syx, sxx, syy

