#!/usr/bin/env python3
"""
Created on Thu Oct 29 10:44:40 2015

@author: Lee Ka Hung
"""

#Current Version 1.1.0
#Updated date: May 24, 2016
#Dihedral Solver
#Program was made to solve dihedral angles of generic systems
#Details on revisions and documentation of input script are in Readme.txt

import os
import pandas as pd
import numpy as np

#Helps you search for the file you desire to use for dihedral angle calculation
class main():
    def mainpd():
        Answer = input('Do you already have the xyzcoords.csv file for angle calculations? y/n ')
        if Answer == 'y':
            main.systemchooser()
        elif Answer == 'n':
            for file in os.listdir():
                if file.endswith(".txt"):
                    if file == "xyzcoords.txt":
                        filename = file
                        print('Reading xyzcoords.txt file...')
                        file = open(filename)
                        break     
                
            #Read file containing xyz coordinates
            xyz = []
                
            #convert txt files into df
            for i in file.readlines():
                i = i.split()
                if len(i) == 4:
                    xyz.append(i[1:4])
            coords = np.asarray(xyz, dtype = float)
            df = pd.DataFrame(data = coords)
                                
            #convert df to csv
            df.to_csv('xyzcoords.csv', sep = ',', float_format = '%+.8e', header = False)
            print('Generating xyzcoords.csv file for angle calculations...')            
            main.systemchooser()
        else:
            print('Please type y for yes or n for no.')
            main.mainpd()
            
    #Reads Input script
    def inputreader():
        script = []
        with open('AngleSolver_Input.txt') as fp:
            for line in fp:
                line = line.split()
                if len(line) == 3:
                    script.append(int(line[2]))
        return script

    #Asks for which system you would like to solve for, foursys or centsys
    def systemchooser():
        scriptinput = main.inputreader()
        System = scriptinput[4] 
        if System == 0:
            main.foursys()
        elif System == 1:
            main.centsys()
        elif System == 2:
            main.pointsys()
        else:
            print('Please check if input is correct for your system. 0 for foursys, 1 for centsys, 2 for pointsys. Re-run code using __main__.py.')
        
    #calculate range of your system
    def rangefinder():
        scriptinput = main.inputreader()
        atoms = scriptinput[0]
        steps = scriptinput[1]
        MDfreq = scriptinput[2]
        numberofparts = scriptinput[3]
        indexrangeofatoms = int((atoms*steps/MDfreq)+(atoms*numberofparts))
        return (atoms, indexrangeofatoms)

    #Solves for the dihedral angle of Atoms 1 to 4  
    def foursys():
        #opens csv file of xyz coordinates        
        df = pd.read_csv('xyzcoords.csv', names = ['x','y','z'])

        #calls rangefinder()
        print('Finding input scripts...')
        (atoms,indexrangeofatoms) = main.rangefinder()
        scriptinput = main.inputreader()

        #atom input
        Atom1 = scriptinput[5]
        Atom2 = scriptinput[6]
        Atom3 = scriptinput[7]
        Atom4 = scriptinput[8]
        
        #generate list of xyz coords for atoms 1, 2, 3, 4
        dfatom1 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom1-1, indexrangeofatoms, atoms))
        dfatom2 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom2-1, indexrangeofatoms, atoms))
        dfatom3 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom3-1, indexrangeofatoms, atoms))
        dfatom4 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom4-1, indexrangeofatoms, atoms))
        
        #reset index to 0
        dfatom1 = dfatom1.reset_index()
        dfatom2 = dfatom2.reset_index()
        dfatom3 = dfatom3.reset_index()
        dfatom4 = dfatom4.reset_index()
        
        #generate df with new resetted index
        dfatom1 = pd.DataFrame(dfatom1, columns = ['x','y','z'])
        dfatom2 = pd.DataFrame(dfatom2, columns = ['x','y','z'])
        dfatom3 = pd.DataFrame(dfatom3, columns = ['x','y','z'])
        dfatom4 = pd.DataFrame(dfatom4, columns = ['x','y','z'])
        
        #generate csv files for each atom
        Answer = input('Do you want xyz coordinates in csv format specifically for your system? y/n? ')
        if Answer == 'y':
            print('Generating csv files...')
            dfatom1.to_csv('atom1.csv', sep=',', float_format='%+.8e', header=False)    
            dfatom2.to_csv('atom2.csv', sep=',', float_format='%+.8e', header=False)
            dfatom3.to_csv('atom3.csv', sep=',', float_format='%+.8e', header=False)
            dfatom4.to_csv('atom4.csv', sep=',', float_format='%+.8e', header=False)
            print('Continuing with calculation...')
        elif Answer == 'n':
            print('Continuing with calculation...')
        else:
            print('Please type y for yes and n for no. Restarting calculation...')
            main.foursys()
            
        #calculate vectors for angle calculation
        veca=np.subtract(dfatom1,dfatom2)
        a = pd.DataFrame(veca)
        vecb=np.subtract(dfatom2,dfatom4)
        b = pd.DataFrame(vecb)
        vecc=np.subtract(dfatom4,dfatom3)
        c = pd.DataFrame(vecc)

        #calls anglesolver
        print('Calculating angles...')
        main.anglesolver(a, b, c)
        print('Calculating distances of points...')
        main.distancefinder(a, b, c)

    #Solves for Dihedral angle of Atom 1, Cent1, Cent2, Atom 7
    def centsys():
        #opens csv file of xyz coordinates        
        df = pd.read_csv('xyzcoords.csv', names = ['x','y','z'])

        #calls rangefinder()
        print('Finding input scripts...')
        (atoms,indexrangeofatoms) = main.rangefinder()
        scriptinput = main.inputreader()
        
        #atom input
        Atom1 = scriptinput[9]
        Atom2 = scriptinput[10]
        Atom3 = scriptinput[11]
        Atom4 = scriptinput[12]
        Atom5 = scriptinput[13]
        Atom6 = scriptinput[14]
        Atom7 = scriptinput[15]
        Atom8 = scriptinput[16]
        Atom9 = scriptinput[17]
        Atom10 = scriptinput[18]
        Atom11 = scriptinput[19]
        Atom12 = scriptinput[20]    
        
        #generate list of xyz coords for atoms 1 to 12
        dfatom1 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom1-1, indexrangeofatoms, atoms))
        dfatom2 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom2-1, indexrangeofatoms, atoms))
        dfatom3 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom3-1, indexrangeofatoms, atoms))
        dfatom4 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom4-1, indexrangeofatoms, atoms))
        dfatom5 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom5-1, indexrangeofatoms, atoms))
        dfatom6 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom6-1, indexrangeofatoms, atoms))
        dfatom7 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom7-1, indexrangeofatoms, atoms))
        dfatom8 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom8-1, indexrangeofatoms, atoms))
        dfatom9 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom9-1, indexrangeofatoms, atoms))
        dfatom10 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom10-1, indexrangeofatoms, atoms))
        dfatom11 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom11-1, indexrangeofatoms, atoms))
        dfatom12 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom12-1, indexrangeofatoms, atoms))
        
        #reset index to 0
        dfatom1 = dfatom1.reset_index()
        dfatom2 = dfatom2.reset_index()
        dfatom3 = dfatom3.reset_index()
        dfatom4 = dfatom4.reset_index()
        dfatom5 = dfatom5.reset_index()
        dfatom6 = dfatom6.reset_index()
        dfatom7 = dfatom7.reset_index()
        dfatom8 = dfatom8.reset_index()
        dfatom9 = dfatom9.reset_index()
        dfatom10 = dfatom10.reset_index()
        dfatom11 = dfatom11.reset_index()
        dfatom12 = dfatom12.reset_index()
        
        #generate df with new resetted index
        dfatom1 = pd.DataFrame(dfatom1, columns = ['x','y','z'])
        dfatom2 = pd.DataFrame(dfatom2, columns = ['x','y','z'])
        dfatom3 = pd.DataFrame(dfatom3, columns = ['x','y','z'])
        dfatom4 = pd.DataFrame(dfatom4, columns = ['x','y','z'])
        dfatom5 = pd.DataFrame(dfatom5, columns = ['x','y','z'])
        dfatom6 = pd.DataFrame(dfatom6, columns = ['x','y','z'])
        dfatom7 = pd.DataFrame(dfatom7, columns = ['x','y','z'])
        dfatom8 = pd.DataFrame(dfatom8, columns = ['x','y','z'])
        dfatom9 = pd.DataFrame(dfatom9, columns = ['x','y','z'])
        dfatom10 = pd.DataFrame(dfatom10, columns = ['x','y','z'])
        dfatom11 = pd.DataFrame(dfatom11, columns = ['x','y','z'])
        dfatom12 = pd.DataFrame(dfatom12, columns = ['x','y','z'])
        
        #generate csv files for each atom
        Answer = input('Do you want xyz coordinates in csv format specifically for your system? y/n? ') 
        if Answer == 'y':
            print('Generating csv files...')
            dfatom1.to_csv('atom1.csv', sep=',', float_format='%+.8e', header=False)    
            dfatom2.to_csv('atom2.csv', sep=',', float_format='%+.8e', header=False)
            dfatom3.to_csv('atom3.csv', sep=',', float_format='%+.8e', header=False)
            dfatom4.to_csv('atom4.csv', sep=',', float_format='%+.8e', header=False)
            dfatom5.to_csv('atom5.csv', sep=',', float_format='%+.8e', header=False)    
            dfatom6.to_csv('atom6.csv', sep=',', float_format='%+.8e', header=False)
            dfatom7.to_csv('atom7.csv', sep=',', float_format='%+.8e', header=False)
            dfatom8.to_csv('atom8.csv', sep=',', float_format='%+.8e', header=False)
            dfatom9.to_csv('atom9.csv', sep=',', float_format='%+.8e', header=False)    
            dfatom10.to_csv('atom10.csv', sep=',', float_format='%+.8e', header=False)
            dfatom11.to_csv('atom11.csv', sep=',', float_format='%+.8e', header=False)
            dfatom12.to_csv('atom12.csv', sep=',', float_format='%+.8e', header=False)
            print('Continuing with calculation...')
        elif Answer == 'n':
            print('Continuing with calculation...')
        else:
            print('Please type y for yes and n for no. Restarting calculation...')
            main.centsys()
            
        #calculate centers of ring structures for angle calculation
        c1 = (dfatom1+dfatom2+dfatom3+dfatom4+dfatom5+dfatom6)/6
        cent1 = pd.DataFrame(c1)
        c2 = (dfatom7+dfatom8+dfatom9+dfatom10+dfatom11+dfatom12)/6
        cent2 = pd.DataFrame(c2)
        
        #calculate vectors for angle calculation
        veca=np.subtract(dfatom1, cent1)
        a = pd.DataFrame(veca)
        vecb=np.subtract(cent1, cent2)
        b = pd.DataFrame(vecb)
        vecc=np.subtract(cent2, dfatom7)
        c = pd.DataFrame(vecc)
        
        #calls anglesolver
        print('Calculating angles...')
        main.anglesolver(a, b, c)
        print('Calculating distances of points...')
        main.distancefinder(a, b, c)

    #Solves for Dihedral angle of Atom 1, Mid1, Mid2, Atom 4
    def pointsys():
        #opens csv file of xyz coordinates        
        df = pd.read_csv('xyzcoords.csv', names = ['x','y','z'])

        #calls rangefinder()
        print('Finding input scripts...')
        (atoms,indexrangeofatoms) = main.rangefinder()
        scriptinput = main.inputreader()
        
        #atom input
        Atom1 = scriptinput[21]
        Atom2 = scriptinput[22]
        Atom3 = scriptinput[23]
        Atom4 = scriptinput[24]
        Atom5 = scriptinput[25]
        Atom6 = scriptinput[26]
        
        #generate list of xyz coords for atoms 1 to 12
        dfatom1 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom1-1, indexrangeofatoms, atoms))
        dfatom2 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom2-1, indexrangeofatoms, atoms))
        dfatom3 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom3-1, indexrangeofatoms, atoms))
        dfatom4 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom4-1, indexrangeofatoms, atoms))
        dfatom5 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom5-1, indexrangeofatoms, atoms))
        dfatom6 = pd.DataFrame(df, columns = ['x','y','z'], index = range(Atom6-1, indexrangeofatoms, atoms))
        
        #reset index to 0
        dfatom1 = dfatom1.reset_index()
        dfatom2 = dfatom2.reset_index()
        dfatom3 = dfatom3.reset_index()
        dfatom4 = dfatom4.reset_index()
        dfatom5 = dfatom5.reset_index()
        dfatom6 = dfatom6.reset_index()
        
        #generate df with new resetted index
        dfatom1 = pd.DataFrame(dfatom1, columns = ['x','y','z'])
        dfatom2 = pd.DataFrame(dfatom2, columns = ['x','y','z'])
        dfatom3 = pd.DataFrame(dfatom3, columns = ['x','y','z'])
        dfatom4 = pd.DataFrame(dfatom4, columns = ['x','y','z'])
        dfatom5 = pd.DataFrame(dfatom5, columns = ['x','y','z'])
        dfatom6 = pd.DataFrame(dfatom6, columns = ['x','y','z'])
        
        #generate csv files for each atom
        Answer = input('Do you want xyz coordinates in csv format specifically for your system? y/n? ') 
        if Answer == 'y':
            print('Generating csv files...')
            dfatom1.to_csv('atom1.csv', sep=',', float_format='%+.8e', header=False)    
            dfatom2.to_csv('atom2.csv', sep=',', float_format='%+.8e', header=False)
            dfatom3.to_csv('atom3.csv', sep=',', float_format='%+.8e', header=False)
            dfatom4.to_csv('atom4.csv', sep=',', float_format='%+.8e', header=False)
            dfatom5.to_csv('atom5.csv', sep=',', float_format='%+.8e', header=False)    
            dfatom6.to_csv('atom6.csv', sep=',', float_format='%+.8e', header=False)
            print('Continuing with calculation...')
        elif Answer == 'n':
            print('Continuing with calculation...')
        else:
            print('Please type y for yes and n for no. Restarting calculation...')
            main.pointsys()
            
        #calculate centers of ring structures for angle calculation
        m1 = (dfatom2+dfatom3)/2
        mid1 = pd.DataFrame(m1)
        m2 = (dfatom5+dfatom6)/2
        mid2 = pd.DataFrame(m2)
        
        #calculate vectors for angle calculation
        veca=np.subtract(dfatom1, mid1)
        a = pd.DataFrame(veca)
        vecb=np.subtract(mid1, mid2)
        b = pd.DataFrame(vecb)
        vecc=np.subtract(mid2, dfatom4)
        c = pd.DataFrame(vecc)
        
        #calls anglesolver
        print('Calculating angles...')
        main.anglesolver(a, b, c)
        print('Calculating distances of points...')
        main.distancefinder(a, b, c)
        
    def anglesolver(a,b,c):
        #cross product calculation
        cp1 = np.cross(a,b)
        cp1 = pd.DataFrame(cp1)
        cp2 = np.cross(b,c)
        cp2 = pd.DataFrame(cp2)
        
        #normalize vectors
        anorm = np.multiply(a,a)
        anorm["suma"] = anorm.sum(axis=1)
        anorm = anorm['suma']
        anorm = np.sqrt(anorm)
        bnorm = np.multiply(b,b)
        bnorm["sumb"] = bnorm.sum(axis=1)
        bnorm = bnorm['sumb']
        bnorm = np.sqrt(bnorm)
        cnorm = np.multiply(c,c)
        cnorm["sumc"] = cnorm.sum(axis=1)
        cnorm = cnorm['sumc']
        cnorm = np.sqrt(cnorm)
        
        #calculate dihedral angles
        norm1 = np.multiply(anorm, bnorm)
        norm1 = pd.DataFrame(norm1)
        n1 = np.divide(cp1, norm1)
        norm2 = np.multiply(bnorm, cnorm)
        norm2 = pd.DataFrame(norm2)
        n2 = np.divide(cp2, norm2)
        bnorm = pd.DataFrame(bnorm)
        bnormvect = np.divide(b,bnorm)
        m1 = np.cross(n1,bnormvect)
        x = np.einsum('ij, ij->i', n1, n2)
        y = np.einsum('ij, ij->i', m1, n2)
        diangle = np.arctan2(y,x)
        degs = np.degrees(diangle)
        print('Calculation finished.')
                
        #generate csv for plot
        degsplot = pd.DataFrame(degs, columns = ['dp'])
        degsplot.to_csv('degsplot.csv', sep=',', float_format='%+.8e', header=False)    
        print('.csv generated for Dihedral Angle.')

    #find distance of a, b, c
    def distancefinder(a, b, c):
        dist_a = np.power(a,2)
        dist_b = np.power(b,2)
        dist_c = np.power(c,2)
        
        dist_a["suma"] = dist_a.sum(axis=1)
        dist_a = dist_a['suma']
        dist_a = np.sqrt(dist_a)
        distaplot = pd.DataFrame(dist_a, columns = ['suma'])
        
        dist_b["sumb"] = dist_b.sum(axis=1)
        dist_b = dist_b['sumb']
        dist_b = np.sqrt(dist_b)
        distbplot = pd.DataFrame(dist_b, columns = ['sumb'])
        
        dist_c["sumc"] = dist_c.sum(axis=1)
        dist_c = dist_c['sumc']
        dist_c = np.sqrt(dist_c)
        distcplot = pd.DataFrame(dist_c, columns = ['sumc'])
                
        #generate csv for plot
        distaplot.to_csv('distplota.csv', sep=',', float_format='%+.8e', header=False)    
        print('.csv generated for a.')

        distbplot.to_csv('distplotb.csv', sep=',', float_format='%+.8e', header=False)    
        print('.csv generated for b.')

        distcplot.to_csv('distplotc.csv', sep=',', float_format='%+.8e', header=False)    
        print('.csv generated for c.')
