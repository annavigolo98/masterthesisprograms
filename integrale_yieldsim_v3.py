import numpy as np
import math as m
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from scipy import integrate
from scipy import optimize as opt
import ROOT

#TGraph for the total stopping power: provided by the function 'write_tot_stopping' below
graphStopPowerNitrogen = ROOT.TGraph( "e_tot_stopping_N.txt" )
graphStopPowerTantalum = ROOT.TGraph( "e_tot_stopping_Ta.txt" )

#Target composition: 1 density (atoms/cm^2), 2 percentage of nitrogen, 3 percentage of tantalum for each sublayer of the target


#COMP LAYERS dec_1
#layer_dx=[0.547524, 0.140000, 0.100000, 0.100000 ] #10^18at/cm^2
#percN=[55.0132, 41.2155 , 12.0000 ,  3.1721  ]
#percTa=[100.-55.0132,100.-41.2155,100.-12.0000,100.-3.1721]

#COMP LAYERS dec_1 prova 1
#layer_dx=[0.887524/10.,0.887524/10.,0.887524/10.,0.887524/10. ,0.887524/10.,0.887524/10.,0.887524/10.,0.887524/10.,0.887524/10.,0.887524/10. ] #10^18at/cm^2
#percN=[42.6,50.1,51.9,52.2,59.7,48.3,41.4,24.4,9.7,3.7 ]
#percTa=[]

#COMP LAYERS dec_1 prova2
layer_dx=[0.887524/30.,0.887524*2./30.,0.887524/10.,0.887524/10.,0.887524/10. ,0.887524/10.,0.887524/10.,0.887524/10.,0.887524/10.,0.887524/10.,0.887524/10. ] #10^18at/cm^2
percN=[31.1,47.6,50.1,51.9,52.2,59.7,48.3,41.4,24.4,9.7,3.7 ]
percTa=[]

for i in range(len(percN)):
   percTa.append(100.-percN[i])



#COMP LAYERS dec_1 fit
#layer_dx=[ 0.08930819164619654 , 0.20886529840734203   ] #10^18at/cm^2
#percN=[  28.028700107292423,41.396862419368325   ]
#percTa=[100.-28.028700107292423   ,100.-41.396862419368325  ]
  
#COMP LAYERS dec_2
   
#layer_dx=[0.100234,0.134804,0.103019,0.229821,0.115302,0.104322,0.111275] #10^18at/cm^2
#percN=[72.6546,53.7575, 53.6916, 47.4629,34.8149, 22.8344, 11.9323    ]
#percTa=[100.-72.6546,100.-53.7575,100.-53.6916,100.-47.4629,100.-34.8149,100.-22.8344, 100.-11.9323]
  
#COMP LAYERS mar_3
#layer_dx=[0.10001,0.27856,0.102153,0.375279,0.202666 ] #10^18at/cm^2
#percN=[29.2815, 42.9672, 32.3414, 20.0711, 6.8396   ]
#percTa=[100.-29.2815,100.-42.9672,100.-32.3414,100.-20.0711,100.-6.8396]



#tools to calculate stopping power for a give energy  E_x; linear interpolation ROOT 


#true stopping power
def stopping_true(ind,E_x): # E_x energy at which we want to calculate the stopping power.

   e_totN14 = graphStopPowerNitrogen.Eval( E_x ) #stopping power totale a E_x per N14
   e_totTa  = graphStopPowerTantalum.Eval( E_x ) #stopping power totale a E_x per Ta
   
   e_true_TaN= 0.01*percN[ind]*e_totN14 + 0.01*percTa[ind]*e_totTa #stopping power true per TaN target
   
   return(e_true_TaN)

# effective stopping power
def stopping_eff(ind,E_x): #ind=index for the layer to be considered, E_x energy for the stopping power and effective stopping power.

  
   e_totN14 = graphStopPowerNitrogen.Eval( E_x ) #stopping power totale a E_x per N14
   e_totTa  = graphStopPowerTantalum.Eval( E_x ) #stopping power totale a E_x per Ta
   
   
   e_eff_TaN= e_totN14 + (percTa[ind]/percN[ind])* e_totTa # effective stopping power in base al layer

   return(e_eff_TaN)

   


#calculates the energy lost in a given target layer (TaN) starting from a given energy E_x

def deltae(ind,E_x): #ind = index of the layer to use, E_x = initial beam energy in the laboratory frame
   
  DE=0.
  

  Xmax = layer_dx[ind] 
  Xmin = 0. #E_1=E-DE
   

  nSteps = 1000


  step = (Xmax - Xmin)/nSteps
   
  E_step=E_x
 
  for i in range( nSteps ):
       stopPower     = stopping_true(ind, E_step) #stopping power in E_step   nel lab
       E_step        -= step*stopPower
  
  
  DE=E_x-E_step
  
  
  return(DE)


#calculates the yield (integral of the cross section over the effective stopping power)  


def integral_L(ind,E_1,E_2):  #ind=index of the layer considered, extrema in energy for the integration


   
   
   a=14./15.
   
   EMax = E_2 #E_2=E
   EMin = E_1 #E_1=E-DE

   
   integral = 0.
    
   
   nSteps = 1000

   
   step = (EMax - EMin)/nSteps

   
   E_step = EMin + step/2  # trapezoid
   #E_step = EMin           # classic method
   
   def calculateCrossSection(E):
     
     T=((0.9893)**2.)/4. #gamma of the resonamce in CM frame 
     E_R=259.56 #keV energy resonance in the CM frame
     
     
     cross=1./((E-E_R)**2.+T)
     return(cross)
     
     
   for i in range( nSteps ):
       stopPower     = stopping_eff(ind, E_step) #stopping power in E_step   in the lab frame
       crossSection  = calculateCrossSection( E_step*a ) #cross section in CM frame
       integral     += step*crossSection/stopPower
       E_step        += step

      
   
   
   return(integral)



    
#writes total stopping power of an element

def write_tot_stopping(e_tot_stopping,E_stopping,name):    
    
    if (name=='N'):
      fout='e_tot_stopping_N.txt'
    if (name=='Ta'):
      fout='e_tot_stopping_Ta.txt'
    #if (name=='Ar'):
    #  fout='e_tot_stopping_Ar.txt'
    #if (name=='15N'):
    #  fout='e_tot_stopping_15N.txt'
        
    f=open(fout,'w')
    
    for i in range(len(E_stoppingN14)): 
        f.write(str(E_stopping[i])+'  '+str(e_tot_stopping[i])+str('\n'))
               
    f.close()
    
#writes effective stopping power for a compound target

def write_eff_stopping(e_totN14,e_totTa,E_stoppingN14):
  
  fout='eff_stoppingTaN_dec_1_simulation.txt'
  f=open(fout,'w')
  
  
  
  for i in range(len(layer_dx)):
  
      e_eff_TaN= e_totN14 + (percTa[i]/percN[i])* e_totTa
      f.write('#Implanted_target_1 (dec_1) \n')
      f.write('#Energy keV, e_effTaN (ev/10^15at/cm^2) \n')
      for i in range(len(E_stoppingN14)): 
             f.write(str(E_stoppingN14[i])+'  '+str(e_eff_TaN[i])+str('\n'))
      f.write("end layer  "+str('\n'))       
  f.close()
     










#MAIN FUNCTION      
# stopping power TaN 
# input files: stopping power calculated from SRIM 2013 

#14N
fname14N='H_in_N14.txt'
E_stoppingN14, e_elN14, e_nucN14 = np.genfromtxt(fname14N,dtype='float',comments='#',usecols=(0,2,3),unpack=True)

e_totN14=e_elN14+e_nucN14

#Ta

fnameTa='H_in_Ta.txt'
E_stoppingTa, e_elTa, e_nucTa = np.genfromtxt(fnameTa,dtype='float',comments='#',usecols=(0,2,3),unpack=True)

e_totTa=e_elTa+e_nucTa

#Ar

#fnameAr='H_in_Ar.txt'
#E_stoppingAr, e_elAr, e_nucAr = np.genfromtxt(fnameAr,dtype='float',comments='#',usecols=(0,2,3),unpack=True)

#e_totAr=e_elAr+e_nucAr


#15N

#fnameN15='H_in_N15.txt'
#E_stopping15N, e_el15N, e_nuc15N = np.genfromtxt(fnameN15,dtype='float',comments='#',usecols=(0,2,3),unpack=True)

#e_tot15N=e_el15N+e_nuc15N


#WRITE STOPPING POWERS
#writes total stopping for N
#name='N'
#write_tot_stopping(e_totN14,E_stoppingN14,name)

#writes total stopping power for Ta
#name='Ta'
#write_tot_stopping(e_totTa,E_stoppingTa,name)


#writes total stopping power for Ar gas
#name='Ar'
#write_tot_stopping(e_totAr,E_stoppingAr,name)



#writes total stopping power for 15N
#name='15N'
#write_tot_stopping(e_tot15N,E_stopping15N,name)


#writes effective  stopping power
#write_eff_stopping(e_totN14,e_totTa,E_stoppingN14)




#energy range for the simulation
E_p=np.arange(275.,300.,0.1) 
Nlayer=len(layer_dx) # number of layers
E_0=275. #minimum value for the energy



a=14./15. #conversion factor from laboratory to CM frame


Yield1=[]  #Yield values

partial_yield=np.zeros([Nlayer,len(E_p)],float)



for i in range(len(E_p)):
    #for every proton energy, calculates the yield
    DE=0. #deltae
    Yield=0.
    
    #extrema for the integral
    
    ext_sup=E_p[i] 
    DE=deltae(0,ext_sup)
    #print("DE_0 ",DE,'\n')
    
    
    ext_inf=E_p[i]-DE
    
    
    for j in range(Nlayer):
      
      
      if(ext_inf<0.):
        #integral from 0 to ext_sup
         
        Yield+=integral_L(j,0.,ext_sup)
        partial_yield[j,i]=integral_L(j,0.,ext_sup)
        #print('break1 \n')
        break   
      
      
      if(ext_inf>=0.):
        #integral from ext_inf to ext_sup
        Yield+= integral_L(j,ext_inf,ext_sup)
        partial_yield[j,i]=integral_L(j,ext_inf,ext_sup) 
        
      if(j==Nlayer-1):
        #print('break2 \n'
        break 
        
        
      ext_sup=ext_inf #E-DE   
      DE=deltae(j+1,ext_sup)
      ext_inf=ext_sup-DE
      
    Yield1.append(Yield)
    

Yield1=np.array(Yield1)







#experimental data
fnamedata='yieldexp2.txt'
a=5./(1.44*1e11) #constant to scale the simulation to the experimental data
E_exp, Y_exp, sigmaY_exp = np.genfromtxt(fnamedata,dtype='float',comments='#',usecols=(0,1,2),unpack=True)


for i in range(Nlayer):
  #plot partial yield for each sublayer
  plt.plot(E_p,partial_yield[i,:]*a,color='black')


#plot 

plt.errorbar(E_exp,Y_exp,sigmaY_exp,fmt='None',color='green',marker='s')
plt.scatter(E_p,Yield1*a,marker='o',s=1)

plt.xlabel('E_p (keV)')
plt.ylabel('Yield (1e-6 atoms)')
plt.show()


fout='Yield_TaN_dec_1_simulation.txt'
f=open(fout,'w')
f.write('#Implanted_target_1 (dec_1) \n')
f.write('#Energy keV, Yield(10^-6 atoms) \n')
for i in range(len(E_p)): 
             f.write(str(E_p[i])+'  '+str(Yield1[i])+'\n')
f.close()






