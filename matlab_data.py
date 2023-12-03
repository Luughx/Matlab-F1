import matlab.engine

class Matlab():
    def __init__(self):
        self.eng = matlab.engine.start_matlab()
    def getPositions(self):
        try:
            self.eng.eval("xi = 1; yi = 285;", nargout=0)

            self.eng.eval("x1 = 130; y1 = 160;", nargout=0)
            self.eng.eval("x2 = 200; y2 = 285;", nargout=0)
            
            self.eng.eval("xf = 475; yf = 255;", nargout=0)

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

            self.eng.eval("yp = @(x) a*(3*x.^2) + b*2*x + c;", nargout=0)
            self.eng.eval("y2p = @(x) 6*a*x + 2*b;", nargout=0)
            self.eng.eval("fun_long = @(x) sqrt(1 + yp(x).^2);", nargout=0)
            self.eng.eval("long_pista2 = integral(fun_long, xi, xf);", nargout=0)

            self.eng.eval("pendientes = yp(x);", nargout=0)
            self.eng.eval("concavidades = y2p(x);", nargout=0)

            self.eng.eval("[maxY, maxX] = max(y);", nargout=0)
            self.eng.eval("maxX = maxX + 10;", nargout=0)
            self.eng.eval("[minY, minX] = min(y);", nargout=0)
            self.eng.eval("minX = minX + 10;", nargout=0)

            self.eng.eval("radio_curvatura = (1 + pendientes.^2).^1.5 ./ abs(concavidades);", nargout=0)
            self.eng.eval("velocidad_c = sqrt(9.8 * radio_curvatura .* ((sind(theta1) + mu * cosd(theta1)) / (cosd(theta1) - mu * sind(theta1))));", nargout=0)
            self.eng.eval("velocidad_c = min(velocidad_c * 3.6, 350);", nargout=0)

            # Cálculos adicionales
            self.eng.eval("energia_potencial = 9.8 * y;", nargout=0)
            self.eng.eval("energia_cinetica = 0.5 * velocidad_c.^2;", nargout=0)
            self.eng.eval("energia_total = energia_potencial + energia_cinetica;", nargout=0)

            self.eng.eval("energia_mecanica = energia_potencial - energia_cinetica;", nargout=0)
            self.eng.eval("fuerza_centripeta = velocidad_c.^2 ./ radio_curvatura;", nargout=0)
            self.eng.eval("fuerza_friction = mu * 9.8 * cosd(theta1);", nargout=0)
            self.eng.eval("trabajo_friccion = fuerza_friction * long_pista2;", nargout=0)
            self.eng.eval("perdida_energia_total = trabajo_friccion;", nargout=0)
           
            # Transformar
            self.eng.eval("velocidad_c_values_vector = cast(velocidad_c, \"single\");", nargout=0) 
            self.eng.eval("radio_curvatura_values_vector = cast(radio_curvatura, \"single\");", nargout=0)
            self.eng.eval("energia_mecanica_values_vector = cast(energia_mecanica, \"single\");", nargout=0)
            self.eng.eval("fuerza_centripeta_values_vector = cast(fuerza_centripeta, \"single\");", nargout=0)
            self.eng.eval("fuerza_friction_values_vector = cast(fuerza_friction, \"single\");", nargout=0)
            self.eng.eval("trabajo_friccion_values_vector = cast(trabajo_friccion, \"single\");", nargout=0)
            self.eng.eval("perdida_energia_total_values_vector = cast(perdida_energia_total, \"single\");", nargout=0)
            self.eng.eval("xValues_vector = cast(x, \"single\");", nargout=0)
            self.eng.eval("yValues_vector = cast(y, \"single\");", nargout=0)

            velocidadCObject = self.eng.eval("velocidad_c_values_vector()", nargout=1)
            radioObject = self.eng.eval("radio_curvatura_values_vector()", nargout=1)
            energiaMecanicaObject = self.eng.eval("energia_mecanica_values_vector()", nargout=1)
            fuerzaCentirpetaObject = self.eng.eval("fuerza_centripeta_values_vector()", nargout=1)
            fuerzaFriccionObject = self.eng.eval("fuerza_friction_values_vector()", nargout=1)
            trabajoFriccionObject = self.eng.eval("trabajo_friccion_values_vector()", nargout=1)
            perdidaTotalObject = self.eng.eval("perdida_energia_total_values_vector()", nargout=1)
            xValuesObject = self.eng.eval("xValues_vector()", nargout=1)
            yValuesObject = self.eng.eval("yValues_vector()", nargout=1)

            velocidadC = matlab.single(velocidadCObject)[0]
            radios = matlab.single(radioObject)[0]
            energiaMecanica = matlab.single(energiaMecanicaObject)[0]
            fuerzaCentripeta = matlab.single(fuerzaCentirpetaObject)[0]
            fuerzaFriccion = matlab.single(fuerzaFriccionObject)[0]
            trabajoFriccion = matlab.single(trabajoFriccionObject)[0]
            perdidaTotal = matlab.single(perdidaTotalObject)[0]
            xValues = matlab.single(xValuesObject)[0]
            yValues = matlab.single(yValuesObject)[0]

            return xValues, yValues, velocidadC, radios, energiaMecanica, fuerzaCentripeta, fuerzaFriccion, trabajoFriccion, perdidaTotal

        except Exception as e:
            print("Error:", str(e))

matlabObject = Matlab()

matlabObject.getPositions()