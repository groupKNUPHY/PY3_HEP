from time import perf_counter                                                                                                               
from numba import jit                                                                                                                       
                                                                                                                                            
                                                                                                                                            
                                                                                                                                            
def pure_sum(n):                                                                                                                            
    result = 0                                                                                                                              
    for i in range(0, n+1):                                                                                                                 
        result += i                                                                                                                         
    return result                                                                                                                           
                                                                                                                                            
@jit(nopython=True, cache=True)                                                                                                             
def numba_sum(n):                                                                                                                           
    result = 0                                                                                                                              
    for i in range(0, n+1):                                                                                                                 
        result += i                                                                                                                         
    return result                                                                                                                           
                                                                                                                                            
                                                                                                                                            
start = perf_counter()                                                                                                                      
pure_sum(100000000)                                                                                                                         
time_normal = perf_counter() - start                                                                                                        
print("normal: ", time_normal)                                                                                                              
                                                                                                                                            
numba_sum(1)                                                                                                                                
                                                                                                                                            
start = perf_counter()                                                                                                                      
numba_sum(100000000)                                                                                                                        
time_numba = perf_counter() - start                                                                                                         
print("numba: ",time_numba)                                  
