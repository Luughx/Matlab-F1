import matlab.engine

class Matlab():
    def __init__(self):
        self.eng = matlab.engine.start_matlab()
    def getPositions(self):
        try:
            self.eng.eval("xi = 2; yi = 300;", nargout=0)

            self.eng.eval("x1 = 130; y1 = 160;", nargout=0)
            self.eng.eval("x2 = 200; y2 = 280;", nargout=0)
            
            self.eng.eval("xf = 500; yf = 300;", nargout=0)

            self.eng.eval("xx = [xi; x1; x2; xf];", nargout=0)
            self.eng.eval("yy = [yi; y1; y2; yf];", nargout=0)

            self.eng.eval("x = xi:xf;", nargout=0)
            self.eng.eval("""m = [xi^3 xi^2 xi 1
                x1^3 x1^2 x1 1
                x2^3 x2^2 x2 1
                xf^3 xf^2 xf 1];""", nargout=0)
            
            self.eng.eval("cofs = m \ [yi; y1; y2; yf];", nargout=0)
            self.eng.eval("a = cofs(1); b = cofs(2); c = cofs(3); d = cofs(4);", nargout=0)
            
            self.eng.eval("f = @(x) a*(x.^3) + b*(x.^2) + c*x + d;", nargout=0)
            self.eng.eval("theta1 = 30;", nargout=0)
            self.eng.eval("theta2 = 45;", nargout=0)
            self.eng.eval("mu = 0.8;", nargout=0)
            self.eng.eval("y = f(x);", nargout=0)

            self.eng.eval("xValues_vector = cast(x, \"single\");", nargout=0)
            self.eng.eval("yValues_vector = cast(y, \"single\");", nargout=0)

            xValuesObject = self.eng.eval("xValues_vector()", nargout=1)
            yValuesObject = self.eng.eval("yValues_vector()", nargout=1)

            xValues = matlab.single(xValuesObject)[0]
            yValues = matlab.single(yValuesObject)[0]

            return xValues, yValues

        except Exception as e:
            print("Error:", str(e))

matlabObject = Matlab()

matlabObject.getPositions()