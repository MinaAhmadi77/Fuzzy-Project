# -*- coding: utf-8 -*-

# python imports
from math import degrees
from time import time

import time

# pyfuzzy imports
#from fuzzy.storage.fcl.Reader import Reader



class FuzzyController:

    def __init__(self, fcl_path):
        #self.system = Reader().load_from_file(fcl_path)
        print("hello")

    def _make_input(self, world):
        return dict(
            cp = world.x,
            cv = world.v,
            pa = degrees(world.theta),
            pv = degrees(world.omega)
        )


    def _make_output(self):
        return dict(
            force = 0.
        )


    def decide(self, world):
        output = self._make_output()
        #self.system.calculate(self._make_input(world), output)
        pa,pv,cv=self.fuzzification(self._make_input(world))
        force = self.defuzzification(self.inference(pa,pv,cv))
        return force     
    def fuzzification(self,data):
        pa = data['pa']
        pv = data['pv']
        cv = data['cv']
        #pa
        up_more_right = 0.0
        if  0.0 <= pa <= 30.0:
            up_more_right = pa / 30

        elif  30.0 <= pa <= 60.0:
            up_more_right = -(pa) / 30 + 2


        up_right = 0.0
        if  30.0 <= pa <=60.0:
            up_right = pa / 30 - 1

        elif  60.0 <= pa <= 90.0:
            up_right = -(pa) / 30 + 3


        up = 0.0
        if 60.0 <= pa <= 90.0:
            up = pa / 30 - 2
        elif  90.0 <= pa <= 120.0:
            up = -(pa) / 30 + 4


        up_left = 0.0
        if  89.0 < pa < 121.0:
            up_left = 1*pa/30-3
        elif 119.0 < pa < 151.0:
            up_left = -(pa)/30 + 5


        up_more_left = 0.0
        if 119.0 < pa < 151.0:
            up_more_left = pa / 30 - 4
        elif 149.0 < pa < 181.0:
            up_more_left = -(pa) / 30 + 6


        down_more_left = 0.0
        if  179.0 < pa < 211.0:
            down_more_left = pa/30-6
        elif 209.0 < pa < 241.0:
            down_more_left = -(pa)/30 + 8


        down_left = 0.0
        if 209.0 < pa < 241.0:
            down_left = pa / 30 - 7
        elif 239.0 < pa < 271.0:
            down_left = -(pa)/30 + 9


        down = 0.0
        if 239.0 < pa < 271.0:
            down = pa / 30 - 8
        elif 269.0 < pa < 301.0:
            down = -(pa) / 30 + 10


        down_right = 0.0
        if  290.0 < pa < 301.0:
            down_right = pa / 30 - 9
        elif  299.0 < pa < 331.0:
            down_right = -(pa)/30 + 11


        down_more_right = 0.0
        if  299.0 < pa < 331.0:
            down_more_right = pa /30 - 10
        elif  329.0 < pa < 361.0:
            down_more_right = -(pa)/30 + 12

        #pv
        cw_fast_pv = 0.0
        if  -201.0 < pv < -99.0:
             cw_fast_pv = -(pv) / 100 - 1
        elif pv < -200.0:
             cw_fast_pv = 1


        cw_slow_pv = 0.0
        if  -201.0 < pv < -99.0:
            cw_slow_pv = pv / 100 + 2
        elif  -99.0 < pv < 1.0:
            cw_slow_pv = -(pv) / 100


        stop_pv = 0.0
        if  -101.0 < pv < 1.0:
            stop_pv = pv / 100 + 1
        elif -1.0 < pv < 101.0:
            stop_pv = -(pv) / 100 + 1


        ccw_slow_pv = 0.0
        if  -1.0 < pv < 101.0:
            ccw_slow_pv = pv / 100
        elif 99.0 < pv < 201.0:
            ccw_slow_pv = -(pv) / 100 + 2


        ccw_fast_pv = 0.0
        if  99.0 < pv < 201.0:
            ccw_fast_pv =pv/100 - 1
        elif pv > 200.0:
            ccw_fast_pv = 1

        return [up_more_right,up_right,up,up_left,up_more_left,down_more_left,down_left,down,down_right,down_more_right],[cw_fast_pv,cw_slow_pv,stop_pv,ccw_slow_pv,ccw_fast_pv],cv

    def inference(self,pa,pv,cv ):
        cv=self.cv_rules(cv)
        for i in range(len(pa)):
            if pa[i]<0:
                pa[i]=abs(0)
            if pa[i]>1:
                pa[i]=1
        for j in range (len(pv)):
            if pv[j]<0:
                pv[j]=abs(0)
            if pv[j]>1:
                pv[j]=1
        dict = {1:0.0,2:0.0,3:0.0,4:0.0,5:0.0}
        # dict[1] = max(min(pa[4],pv[1]),min(pa[4],pv[3]),min(pa[4],pv[4]),min(pa[5],pv[1]),min(pa[6],pv[1]),min(pa[6],pv[3]),min(pa[3],pv[3]),min(pa[3],pv[2]),min(pa[2],pv[4]),min(pa[1],pv[4]),min(pa[3],pv[4]))
        # dict[2] = max(min(pa[0],pv[4]),min(pa[2],pv[3]),min(pa[3],pv[1]),min(pa[6],pv[4]))
        # dict[3] = max(min(pa[2],pv[2]),min(pa[1],pv[3]),min(pa[3],pv[1]),min(pa[5],pv[0]),min(pa[5],pv[3]),min(pa[5],pv[4]),min(pa[9],pv[0]),min(pa[9],pv[1]),min(pa[9],pv[4]),min(pa[8],pv[4]),min(pa[6],pv[0]),min(pa[7],pv[4]),min(pa[7],pv[0]))
        # dict[4] = max(min(pa[4],pv[0]),min(pa[8],pv[0]),min(pa[1],pv[3]),min(pa[2],pv[1]))
        # dict[5] = max(min(pa[0],pv[1]),min(pa[0],pv[3]),min(pa[0],pv[0]),min(pa[9],pv[3]),min(pa[8],pv[1]),min(pa[8],pv[3]),min(pa[1],pv[1]),min(pa[1],pv[2]),min(pa[1],pv[0]),min(pa[3],pv[0]),min(pa[7],pv[2]),min(pa[2],pv[0]))
        dict[1] = max(min(pa[0],pv[4],cv[1]),min(pa[4],pv[4],cv[1]),min(pa[6],pv[1]),min(pa[6],pv[3]),min(pa[3],pv[3]),min(pa[3],pv[2]),min(pa[2],pv[4]),min(pa[1],pv[4]),min(pa[3],pv[4]))
        dict[2] = max(min(pa[5],pv[1],cv[1]),min(pa[4],pv[3],cv[0]),min(pa[4],pv[1],cv[0]),min(pa[2],pv[3]),min(pa[3],pv[1]),min(pa[6],pv[4]))
        dict[3] = max(min(pa[2],pv[2]),min(pa[1],pv[3]),min(pa[3],pv[1],cv[2]),min(pa[5],pv[0]),min(pa[5],pv[3]),min(pa[5],pv[4]),min(pa[9],pv[0]),min(pa[9],pv[1]),min(pa[9],pv[4]),min(pa[8],pv[4]),min(pa[6],pv[0]),min(pa[7],pv[4]),min(pa[7],pv[0]))
        dict[4] = max(min(min(pa[1],pv[1],cv[4]),pa[0],pv[3],cv[3]),min(pa[4],pv[0]),min(pa[8],pv[0]),min(pa[1],pv[3]),min(pa[2],pv[1]))
        dict[5] = max(min(pa[9],pv[3]),min(pa[8],pv[1]),min(pa[8],pv[3]),min(pa[1],pv[2]),min(pa[1],pv[0]),min(pa[3],pv[0]),min(pa[7],pv[2]),min(pa[2],pv[0]))

        return dict

    def defuzzification(self,fset):
        
        

        n=10000
        de= 200. /n
        resolution=[-100. + i*de for i in range(n+1)]
        y=0.0
        x_centroid = 0.0
        for x in resolution:
            y += self.membership(x,fset) * x * de
            x_centroid += self.membership(x,fset) * de
        try:
            f=y/x_centroid
        except ZeroDivisionError:
            f=0
        return f

    def membership(self,x,fset):
        ll=[]
        ll.append(self.force_left_fast(x))
        ll.append(self.force_left_slow(x))
        ll.append(self.force_stop(x))
        ll.append(self.force_right_slow(x))
        ll.append(self.force_right_fast(x))

        if ll[0] >= fset[1]:
            ll[0]=fset[1]
        if ll[1] >= fset[2]:
            ll[1]=fset[2]
        if ll[2] >= fset[3]:
            ll[2] = fset[3]
        if ll[3] >= fset[4]:
            ll[3] = fset[4]
        if ll[4] >= fset[5]:
            ll[4] = fset[5]

        if fset[1]==0:
            ll[0]=0
        if fset[2]==0:
            ll[1]=0
        if fset[3]==0:
            ll[2]=0
        if fset[4]==0:
            ll[3]=0
        if fset[5]==0:
            ll[4]=0

        return max(ll[0],ll[1],ll[2],ll[3],ll[4])

    def trimf (self,x, par):

        a = par[0]
        b = par[1]
        c = par[2]

        result=a


        return result

    #force
    def force_left_fast(self,x):
        result = 0.0
        if  -100.0 <= x <= -80.0:
            result = x / 20 + 5
        elif  -88.0 <= x <= -60.0:
            result = -1*x /20 - 3
        return result
    def force_left_slow(self,x):
        result=0.0
        if -80.0<= x <= -60.0:
            result = x / 20 + 4
        elif -60.0 <= x <= 0.0:
            result = -1*x / 60
        return result
    def force_stop(self,x):
        result = 0.0
        if  -60.0 <= x <= 0.0:
            result = x / 60 + 1
        elif  0.0 <= x <= 60.0:
            result = -1*x / 60 + 1
        return result

    def force_right_slow(self,x):
        result = 0.0
        if  0<= x <= 60:
            result = x / 60
        elif  60 <= x <= 80:
            result = -1*x / 20 + 4
        return result

    def force_right_fast(self,x):
        result = 0.0
        if  60.0 <= x <= 80.0:
            result =x/ 20 - 3
        elif  80.0 <= x <= 100.0:
            result = -1*x / 20 + 5
        return result

    def cv_rules(self,data):
        cv=data

        left_fast= 0.0
        if -6.0 < cv <= -2.5:
            left_fast = -(cv)/2.5-1

        left_slow = 0.0
        if  -6.0 < cv < 0.0:
            left_slow= cv/4+5/4

        elif -2.0 < cv < 1.0:
            left_slow = -(cv)

        stop = 0.0
        if -2.0 < cv < 1.0:
            stop = cv+1

        elif -1.0 < cv < 2.0:
            stop= -(cv) +1

        right_slow = 0.0
        if  -1.0 < cv < 2.0:
            right_slow =cv

        elif  0.0 < cv < 6.0:
            right_slow= -1*cv/4+5/4


        right_fast = 0.0
        if cv >= 2.5 <  cv < 6.0:
            right_fast = cv/2.5 - 1

        return [left_fast,left_slow, stop, right_slow, right_fast]