#input:
#previous parameter e1 e2 e3 e4 e5 e6.
#xPrice can be close price typical price could be (High + Low + Close)/3
#SMA: 14-period Simple moving average
#MD: Mean Deviation
# output 1 buy, 0 sell, data for next iteration
#[signal,parameter xccir, e1,e2,e3,e4,e5,e6 for next iteration.


def t3_cci(e1_pre,e2_pre,e3_pre,e4_pre,e5_pre,e6_pre,xPrice,SMA,MD):

    CCI_Period = 14 # # of bars simple moving average
    T3_Period = 5 # # of bars for T3
    b = 0.618 # constant
     
    b2 = b*b
    b3 = b2*b
    c1 = -b3
    c2 = (3*(b2 + b3))
    c3 = -3*(2*b2 + b + b3)
    c4 = (1 + 3*b + b3 + 3*b2)
    nn = 0

    if (T3_Period < 1):
        nn = 1
    else:
        nn = T3_Period

    nr = 1 + 0.5*(nn - 1)
    w1 = 2 / (nr + 1)
    w2 = 1 - w1    

    xcci = (xPrice-SMA)/(0.015*MD) # function f_CCI input xPRice and CCI_Period, output constant
    print(xcci)
    e1 = w1*xcci + w2*e1_pre
    e2 = w1*e1 + w2*e2_pre
    e3 = w1*e2 + w2*e3_pre
    e4 = w1*e3 + w2*e4_pre
    e5 = w1*e4 + w2*e5_pre
    e6 = w1*e5 + w2*e6_pre

    xccir = c1*e6 + c2*e5 + c3*e4 + c4*e3  

    if (xccir >=0):
        signal = 1
    else:
        signal = 0

    result = [signal,xccir,e1,e2,e3,e4,e5,e6]
    
    return(result) 



