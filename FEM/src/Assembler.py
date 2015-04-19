import scipy, scipy.sparse
import Function, Integrator

def precomputeMatrices(slopeFunctions, parameters):
    G = scipy.sparse.lil_matrix((parameters.n, parameters.n))
    A = scipy.sparse.lil_matrix((parameters.n, parameters.n))
    BPrime = scipy.sparse.lil_matrix((parameters.n, parameters.n))
      
    for element in parameters.omega:
        for i in range(0,3):
            for j in range(0,3):
                #Get the points
                xi = element.points[i]
                xj = element.points[j]
                
                #Get slope functions
                slopeI = slopeFunctions[element.index][i]
                slopeJ = slopeFunctions[element.index][j]
                                
                #Compute G matrix
                fI = Function.FunctionWrapper(slopeI.evaluate, str(slopeI))
                fJ = Function.FunctionWrapper(slopeJ.evaluate, str(slopeJ))
                f = fI * fJ
                I = Integrator.integrate2D(f, element)
                G[xi.index, xj.index] += I
    
                #Compute A matrix
                sum = 0
                slopeIDerivates = slopeI.getDerivates()
                slopeJDerivates = slopeJ.getDerivates()
                for l in range(0,2):
                    for k in range(0,2):
                        #a_lk
                        tensor = Function.FunctionWrapper(parameters.diffusionTensor[l][k], "a_" + str(l) + str(k))
                        #vj/dx_k 
                        derivate1 = Function.FunctionWrapper(slopeJDerivates[k], "v" + str(xj.index) + "/dx_" + str(k))
                        #vi/dx_l            
                        derivate2 = Function.FunctionWrapper(slopeIDerivates[l], "v" + str(xi.index) + "/dx_" + str(l))
                        f = tensor * derivate1 * derivate2
                        I = Integrator.integrate2D(f, element)
                        sum += I
                A[xi.index, xj.index] -= sum
    
    #Lump the G matrix
    for i in range(0, parameters.n):
        sum = 0
        for j in range(0, parameters.n):
            sum += G[i,j]
            G[i,j] = 0
        G[i,i] = sum
    
    for boundarySegmentDesc in parameters.omegaD:
        segment = boundarySegmentDesc[0]
        element = boundarySegmentDesc[1]
        for i in range(0,2):
            for j in range(0,2):
                xi = segment.points[i]
                xj = segment.points[j]
                slopeI = slopeFunctions[element.index][element.pointToElementIndex(xi)]
                slopeJ = slopeFunctions[element.index][element.pointToElementIndex(xj)]
                fI = Function.FunctionWrapper(slopeI.evaluate, str(slopeI))
                fJ = Function.FunctionWrapper(slopeJ.evaluate, str(slopeJ))
                f = fI * fJ
                I = Integrator.integrate1D(f, segment)
                BPrime[xj.index, xi.index] -= I
                
    return (G.tocsc(), A.tocsc(), BPrime.tocsc())

def computeProductionVector(z, slopeFunctions, parameters):
    #Return value
    P = scipy.sparse.lil_matrix((parameters.n, 1))
    
    #Functions
    beta = Function.FunctionWrapper(parameters.productionEffciency, "B")
    rho = Function.ConstantFunction(parameters.productionThreshold)
    
    #For each element
    for element in parameters.omegaThree:
        #Build a sum of non-zero functions on this element       
        sum = Function.ConstantFunction(0)
        for i in range(0,3):
            #Get the point
            xi = element.points[i]
            #The coefficient
            zl = z[xi.index, 0]
            #The shape function
            slopeL = slopeFunctions[element.index][i]
            
            zFunction = Function.ConstantFunction(zl)
            slopeLWrapper = Function.FunctionWrapper(slopeL.evaluate, str(slopeL))
            sumElement = zFunction * slopeLWrapper
            sum = sum + sumElement
            
        #Build a 'B(x)(rho - sum)+' term
        g = beta * Function.PositivePartFunction(rho - sum)
        
        #Integrate
        for i in range(0,3):
            xi = element.points[i]
            slopeK = slopeFunctions[element.index][i]
            slopeKWrapper = Function.FunctionWrapper(slopeK.evaluate, str(slopeK))
            h = g * slopeKWrapper
            I = Integrator.integrate2D(h, element)
            P[xi.index, 0] += I
      
    return P.tocsc()
            
            
