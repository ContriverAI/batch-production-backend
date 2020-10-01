def softner_t1(str1):
    print("----------{}-----".format(str1))
    if str1[-2:] == "AM" and str1[:2] == "12": 
        return "00" + str1[2:-2] 
          
    # remove the AM     
    elif str1[-2:] == "AM": 
        return str1[:-2] 
      
    # Checking if last two elements of time 
    # is PM and first two elements are 12    
    elif str1[-2:] == "PM" and str1[:2] == "12": 
        return str1[:-2] 
          
    else:
        return str(int(str1[:1]) + 12) + str1[2:8]

print(softner_t1("01:05 PM"))