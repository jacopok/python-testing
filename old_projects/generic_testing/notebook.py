# %%markdown
#
# # SymPy
#
# `SymPy` is a package for symbolic calculations in python,
# similar to *Mathematica*. It works with expressions containing symbols.
# $2 \pi e^{i\pi}$
# %%
# from sympy import *
# init_printing()
# %% markdown
# Symbols are basic bricks used to construct expressions.
# Each symbol has a name used for printing expressions. Objects of the class `Symbol` should be created and assigned to python variables in order to be used in expressions. The symbol name and the name of the variable to which this symbol is assigned are two independent things, and one may write `abc=Symbol('xyz')`. But then one has to write `abc` in input expressions, while `SymPy` will write `xyz` in output ones, producing unnecessary confusion. The python variable name should better be the same as the symbol name.
#
# In languages specifically designed for symbolic calculations, such as *Mathematica*, if a variable to which nothing has been assigned is used, it automatically means a symbol with the same name. Python has not been designed for symbolic calculations. If you use a variable to which nothing has been assigned, you will get an error message. Symbol objects have to be created explicitly.
# %%
x=Symbol('x')
# %%
a=x**2-1
a
# %% markdown
# Several symbols can be defined at once. The string is split at spaces.
# %%
y,z=symbols('y z')
# %% markdown
# Let's substitute $y+1$ for $x$.
# %%
a.subs(x,y+1)
# %% markdown
# ## Polynomials and rational functions
#
# `SymPy` does not expand brackets automatically. The function `expand` is used for this.
# %%
a=(x+y-z)**6
a
# %%
a=expand(a)
a
# %% markdown
# Degree of the polynomial $a$ in $x$.
# %%
degree(a,x)
# %% markdown
# Let's collect terms with same power of $x$ together.
# %%
collect(a,x)
# %% markdown
# Any polynomial with integer coefficients can be factorized into polynomials with integer coefficients (which cannot be factorized further). There exist efficient algorithms to do this.
# %%
a=factor(a)
a
# %% markdown
# `SymPy` does not automatically cancel ratios of polynomials by their greatest common divisor. The function `cancel` is used for this.
# %%
a=(x**3-y**3)/(x**2-y**2)
a
# %%
cancel(a)
# %% markdown
# `SymPy` does not automatically bring sums of rational expressions to common denominator. The function `together` is used for this.
# %%
a=y/(x-y)+x/(x+y)
a
# %%
together(a)
# %% markdown
# The function `simplify` tries to rewrite an expression *in a simplest form*. This concept is not well defined (different forms may be considered simplest in different contexts), and there exists no algorithm for such simplification. The function `simplify` works heuristically, and it is not possible to guess in advance what simplifications it will try. It is very convenient in interactive sessions in order to check if it will succeed in rewriting an expression in some reasonably good form. But it is not desirable to use it in programs. There one should better use more specialized functions which perform well defined expression transformations.
# %%
simplify(a)
# %% markdown
# Partial fraction decomposition with respect to $x$.
# %%
apart(a,x)
# %% markdown
# Let's substitute some values for the symbils $x$ and $y$.
# %%
a=a.subs({x:1,y:2})
a
# %% markdown
# And how much is it numerically?
# %%
a.n()
# %% markdown
# ## Elementary functions
#
# `SymPy` automatically applies simplifications of elementary functions which are correct everywhere.
# %%
sin(-x)
# %%
cos(pi/4),tan(5*pi/6)
# %% markdown
# `SymPy` can work with floating point numbers having arbitrarily high precision. Here is $\pi$ with 100 significant digits.
# %%
pi.n(100)
# %% markdown
# `E` is the base of natural logarithms.
# %%
log(1),log(E)
# %%
exp(log(x)),log(exp(x))
# %% markdown
# Why not $x$? Try $x=2\pi i$.
# %%
sqrt(0)
# %%
sqrt(x)**4,sqrt(x**4)
# %% markdown
# Why not $x^2$? Try $x=i$.
#
# Symbols can have certain properties. E.g., they can be positive. Then `SymPy` can simplify square roots better.
# %%
p,q=symbols('p q',positive=True)
sqrt(p**2)
# %%
sqrt(12*x**2*y),sqrt(12*p**2*y)
# %% markdown
# Let the symbol $n$ be integer (`I` is the imaginary unit).
# %%
n=Symbol('n',integer=True)
exp(2*pi*I*n)
# %% markdown
# The method `rewrite` tries to rewrite an expression in terms of a given function.
# %%
cos(x).rewrite(exp),exp(I*x).rewrite(cos)
# %%
asin(x).rewrite(log)
# %% markdown
# The function `trigsimp` tries to rewrite a trigonometric expression *in a simplest form*. In programs it is better to use more specialized functions.
# %%
trigsimp(2*sin(x)**2+3*cos(x)**2)
# %% markdown
# The function `expand_trig` expands sines and cosines of sums and multiple angles.
# %%
expand_trig(sin(x-y)),expand_trig(sin(2*x))
# %% markdown
# The inverse transformation, rewriting products and powers of sines and cosines into expressions linear in these functions, is needed more often. Suppose we work with a truncated Fourier series.
# %%
a1,a2,b1,b2=symbols('a1 a2 b1 b2')
a=a1*cos(x)+a2*cos(2*x)+b1*sin(x)+b2*sin(2*x)
a
# %% markdown
# We want to square it and get a truncated Fourier series again.
# %%
a=(a**2).rewrite(exp).expand().rewrite(cos).expand()
a
# %%
a.collect([cos(x),cos(2*x),cos(3*x),sin(x),sin(2*x),sin(3*x)])
# %% markdown
# The function `expand_log` transforms logarithms of products and powers (of positive quantities) into sums of logarithms; `logcombine` performs the inverse transformation.
# %%
a=expand_log(log(p*q**2))
a
# %%
logcombine(a)
# %% markdown
# The function `expand_power_exp` rewrites powers whose exponents are sums via products of powers.
# %%
expand_power_exp(x**(p+q))
# %% markdown
# The function `expand_power_base` rewrites powers whose bases are products via products of powers.
# %%
expand_power_base((x*y)**n)
# %% markdown
# The function `powsimp` performs the inverse transformations.
# %%
powsimp(exp(x)*exp(2*y)),powsimp(x**n*y**n)
# %% markdown
# New symbolic functions can be introduced. They may have an arbitrary numbers of arguments.
# %%
f=Function('f')
f(x)+f(x,y)
# %% markdown
# ## Expression structure
#
# Internally expressions are are trees. The function `srepr` returns a string representing this tree.
# %%
srepr(x+1)
# %%
srepr(x-1)
# %%
srepr(x-y)
# %%
srepr(2*x*y/3)
# %%
srepr(x/y)
# %% markdown
# One may use the functions `Add`, `Mul`, `Pow`, etc. instead of the binary operations `+`, `*`, `**`, etc.
# %%
Mul(x,Pow(y,-1))
# %%
srepr(f(x,y))
# %% markdown
# The attribute `func` is the top-level function of an expression, and `args` is the list of its agruments.
# %%
a=2*x*y**2
a.func
# %%
a.args
# %%
for i in a.args:
    print(i)
# %% markdown
# The function `subs` substitutes an expression for a symbol.
# %%
a.subs(y,2)
# %% markdown
# It can perform substitutions for several symbols. To this end, one calls it with a list of tuples or a dictionary.
# %%
a.subs([(x,pi),(y,2)])
# %%
a.subs({x:pi,y:2})
# %% markdown
# It can substitute not only for a symbol but also for a subexpression - a function with arguments.
# %%
a=f(x)+f(y)
a.subs(f(y),1)
# %%
(2*x*y*z).subs(x*y,z)
# %%
(x+x**2+x**3+x**4).subs(x**2,y)
# %% markdown
# Substitutions are performed sequentially. In this case, first $x$ is replaced by $y$ producing $y^3+y^2$; then $y$ is replaced by $x$ in this result.
# %%
a=x**2+y**3
a.subs([(x,y),(y,x)])
# %% markdown
# Interchanging these substitutions leads to a different result.
# %%
a.subs([(y,x),(x,y)])
# %% markdown
# But if one calls `subs` with the keyword parameter `simultaneous=True`, all substitutions are preformed simultaneously. In this way one can, e.g., interchange $x$ and $y$.
# %%
a.subs([(x,y),(y,x)],simultaneous=True)
# %% markdown
# A function can be replaced by another function.
# %%
g=Function('g')
a=f(x)+f(y)
a.subs(f,g)
# %% markdown
# The method `replace` searches for subexpressions matching a pattern (with wildcards) and replaces them by a given expression.
# %%
a=Wild('a')
(f(x)+f(x+y)).replace(f(a),a**2)
# %%
(f(x,x)+f(x,y)).replace(f(a,a),a**2)
# %%
a=x**2+y**2
a.replace(x,x+1)
# %% markdown
# Only a complete subtree can match a pattern, not a subset of factors in a product or a smaller power in a larger one.
# %%
a=2*x*y*z
a.replace(x*y,z)
# %%
(x+x**2+x**3+x**4).replace(x**2,y)
# %% markdown
# ## Solving equations
# %%
a,b,c,d,e,f=symbols('a b c d e f')
# %% markdown
# An equation is represented by the function `Eq` with two arguments. The function `solve` returns a list of solutions.
# %%
solve(Eq(a*x,b),x)
# %% markdown
# Instead of equations, one may pass just expressions to `solve`;
# they mean equations `<expression>=0`.
# %%
solve(a*x+b,x)
# %% markdown
# A square equation has 2 solutions.
# %%
solve(a*x**2+b*x+c,x)
# %% markdown
# A system of linear equations.
# %%
solve([a*x+b*y-e,c*x+d*y-f],[x,y])
# %% markdown
# The function `roots` returns roots of a polynomial together with their multiplicities.
# %%
roots(x**3-3*x+2,x)
# %% markdown
# The function `solve_poly_system` solves systems of polynomial equations by constructing their Gröbner bases.
# %%
p1=x**2+y**2-1
p2=4*x*y-1
solve_poly_system([p1,p2],x,y)
# %% markdown
# ## Series
# %%
exp(x).series(x,0,5)
# %% markdown
# A series can start from a negative power.
# %%
cot(x).series(x,n=5)
# %% markdown
# And even run over half-integer powers.
# %%
sqrt(x*(1-x)).series(x,n=5)
# %%
log(gamma(1+x)).series(x,n=6).rewrite(zeta)
# %% markdown
# Let's prepare 3 series.
# %%
sinx=series(sin(x),x,0,8)
sinx
# %%
cosx=series(cos(x),x,n=8)
cosx
# %%
tanx=series(tan(x),x,n=8)
tanx
# %% markdown
# Products and ratios of series are not calculated automatically, the function `series` should be applied to them.
# %%
series(tanx*cosx,n=8)
# %%
series(sinx/cosx,n=8)
# %% markdown
# And this series should be equal to 1. But since `sinx` and `cosx` are known only with a limited accuracy, we obtain 1 with the same accuracy.
# %%
series(sinx**2+cosx**2,n=8)
# %% markdown
# Here the leading terms have canceled, and the result can be obtained only with a lower accuracy.
# %%
series((1-cosx)/x**2,n=6)
# %% markdown
# Series can be differentiated and integrated.
# %%
diff(sinx,x)
# %%
integrate(cosx,x)
# %% markdown
# A series (starting from a small term) can be substituted for an expansion variable in another series. Here are $\sin(\tan(x))$ and $\tan(\sin(x))$.
# %%
st=series(sinx.subs(x,tanx),n=8)
st
# %%
ts=series(tanx.subs(x,sinx),n=8)
ts
# %%
series(ts-st,n=8)
# %% markdown
# It is not possible to substitute a numerical value for the expansion variable in a series (and hence to plot it). To this end one has to remove the $\mathcal{O}$ term first, transforming a series into a polynomial.
# %%
sinx.removeO()
# %% markdown
# ## Derivatives
# %%
a=x*sin(x+y)
diff(a,x)
# %%
diff(a,y)
# %% markdown
# The second derivative in $x$ and the first one in $y$.
# %%
diff(a,x,2,y)
# %% markdown
# Expressions with undefined functions can be differentiated.
# %%
a=x*f(x**2)
b=diff(a,x)
b
# %% markdown
# What's this?
# %%
print(b)
# %% markdown
# The function `Derivative` represents an unevaluated derivative. It can be evaluated by the method `doit`.
# %%
a=Derivative(sin(x),x)
Eq(a,a.doit())
# %% markdown
# ## Integrals
# %%
integrate(1/(x*(x**2-2)**2),x)
# %%
integrate(1/(exp(x)+1),x)
# %%
integrate(log(x),x)
# %%
integrate(x*sin(x),x)
# %%
integrate(x*exp(-x**2),x)
# %%
a=integrate(x**x,x)
a
# %% markdown
# This is an unevaluated integral.
# %%
print(a)
# %%
a=Integral(sin(x),x)
Eq(a,a.doit())
# %% markdown
# Definite integrals.
# %%
integrate(sin(x),(x,0,pi))
# %% markdown
# `oo` means $\infty$.
# %%
integrate(exp(-x**2),(x,0,oo))
# %%
integrate(log(x)/(1-x),(x,0,1))
# %% markdown
# ## Summing series
# %%
summation(1/n**2,(n,1,oo))
# %%
summation((-1)**n/n**2,(n,1,oo))
# %%
summation(1/n**4,(n,1,oo))
# %% markdown
# An unevaluated sum is denoted `Sum`.
# %%
a=Sum(x**n/factorial(n),(n,0,oo))
Eq(a,a.doit())
# %% markdown
# ## Limits
# %%
limit((tan(sin(x))-sin(tan(x)))/x**7,x,0)
# %% markdown
# This limit is easy: just expand the numerator and the denominator into series. Things become more difficult if $x=0$ is an essential singularity. Let's calculate one-sided limits.
# %%
limit((tan(sin(x))-sin(tan(x)))/(x**7+exp(-1/x)),x,0,'+')
# %%
limit((tan(sin(x))-sin(tan(x)))/(x**7+exp(-1/x)),x,0,'-')
# %% markdown
# ## Differential equations
# %%
t=Symbol('t')
x=Function('x')
p=Function('p')
# %% markdown
# First order.
# %%
dsolve(diff(x(t),t)+x(t),x(t))
# %% markdown
# Second order.
# %%
dsolve(diff(x(t),t,2)+x(t),x(t))
# %% markdown
# A system of first-order equations.
# %%
dsolve((diff(x(t),t)-p(t),diff(p(t),t)+x(t)))
# %% markdown
# ## Linear algebra
# %%
a,b,c,d,e,f=symbols('a b c d e f')
# %% markdown
# A matrix can be constructed from a list of lists.
# %%
M=Matrix([[a,b,c],[d,e,f]])
M
# %%
M.shape
# %% markdown
# A row matrix.
# %%
Matrix([[1,2,3]])
# %% markdown
# A column matrix.
# %%
Matrix([1,2,3])
# %% markdown
# A matrix can be constructed from a function.
# %%
def g(i,j):
    return Rational(1,i+j+1)
Matrix(3,3,g)
# %% markdown
# Or from an undefined function.
# %%
g=Function('g')
M=Matrix(3,3,g)
M
# %%
M[1,2]
# %%
M[1,2]=0
M
# %%
M[2,:]
# %%
M[:,1]
# %%
M[0:2,1:3]
# %% markdown
# A unit matrix.
# %%
eye(3)
# %% markdown
# A zero matrix.
# %%
zeros(3)
# %%
zeros(2,3)
# %% markdown
# A diagonal matrix.
# %%
diag(1,2,3)
# %%
M=Matrix([[a,1],[0,a]])
diag(1,M,2)
# %% markdown
# Operations with matrices.
# %%
A=Matrix([[a,b],[c,d]])
B=Matrix([[1,2],[3,4]])
A+B
# %%
A*B,B*A
# %%
A*B-B*A
# %%
simplify(A**(-1))
# %%
det(A)
# %% markdown
# ### Eigenvalues and eigenvectors
# %%
x=Symbol('x',real=True)
# %%
M=Matrix([[(1-x)**3*(3+x),4*x*(1-x**2),-2*(1-x**2)*(3-x)],
          [4*x*(1-x**2),-(1+x)**3*(3-x),2*(1-x**2)*(3+x)],
          [-2*(1-x**2)*(3-x),2*(1-x**2)*(3+x),16*x]])
M
# %%
det(M)
# %% markdown
# This means that this matrix has a null space (this matrix transforms vectors from this subspace into 0). Let's find a basis of this subspace.
# %%
v=M.nullspace()
len(v)
# %% markdown
# It is one-dimensional.
# %%
v=simplify(v[0])
v
# %% markdown
# Let's check.
# %%
simplify(M*v)
# %% markdown
# The eigenvalues and their multiplicities.
# %%
M.eigenvals()
# %% markdown
# If both eigenvalues and corresponding eigenvectors are needed, the method `eigenvects` is used. It returns a list of tuples. In each tuple the zeroth element is an eigenvalue, the first one is its multiplicity, and the last one is a list of corresponding basis eigenvectors (their number is the multiplicity).
# %%
v=M.eigenvects()
len(v)
# %%
for i in range(len(v)):
    v[i][2][0]=simplify(v[i][2][0])
v
# %% markdown
# Let's check.
# %%
for i in range(len(v)):
    z=M*v[i][2][0]-v[i][0]*v[i][2][0]
    pprint(simplify(z))
# %% markdown
# ### Jordan normal form
# %%
M=Matrix([[Rational(13,9),-Rational(2,9),Rational(1,3),Rational(4,9),Rational(2,3)],
          [-Rational(2,9),Rational(10,9),Rational(2,15),-Rational(2,9),-Rational(11,15)],
          [Rational(1,5),-Rational(2,5),Rational(41,25),-Rational(2,5),Rational(12,25)],
          [Rational(4,9),-Rational(2,9),Rational(14,15),Rational(13,9),-Rational(2,15)],
          [-Rational(4,15),Rational(8,15),Rational(12,25),Rational(8,15),Rational(34,25)]])
M
# %% markdown
# The method `M.jordan_form()` returns a couple of matrices, the transformation matrix $P$ and the Jordan form $J$: $M = P J P^{-1}$.
# %%
P,J=M.jordan_form()
J
# %%
P=simplify(P)
P
# %% markdown
# Let's check.
# %%
Z=P*J*P**(-1)-M
simplify(Z)
# %% markdown
# ## Plots
#
# `SymPy` uses `matplotlib`. However, it distributes $x$ points adaptively, not uniformly.
# %%
%matplotlib inline
# %% markdown
# A single function.
# %%
plot(sin(x)/x,(x,-10,10))
# %% markdown
# Several functions.
# %%
plot(x,x**2,x**3,(x,0,2))
# %% markdown
# Some additional plotting functions can be imported from `sympy.plotting`.
# %%
from sympy.plotting import (plot_parametric,plot_implicit,
                            plot3d,plot3d_parametric_line,
                            plot3d_parametric_surface)
# %% markdown
# A parametric plot - a Lissajous curve.
# %%
t=Symbol('t')
plot_parametric(sin(2*t),cos(3*t),(t,0,2*pi),
                title='Lissajous',xlabel='x',ylabel='y')
# %% markdown
# An implicit plot - a circle.
# %%
plot_implicit(x**2+y**2-1,(x,-1,1),(y,-1,1))
# %% markdown
# A surface. If it is not inline but in a separaye window, you can rotate it with your mouse.
# %%
plot3d(x*y,(x,-2,2),(y,-2,2))
# %% markdown
# Several surfaces.
# %%
plot3d(x**2+y**2,x*y,(x,-2,2),(y,-2,2))
# %% markdown
# A parametric space curve - a spiral.
# %%
a=0.1
plot3d_parametric_line(cos(t),sin(t),a*t,(t,0,4*pi))
# %% markdown
# A parametric surface - a torus.
# %%
u,v=symbols('u v')
a=0.3
plot3d_parametric_surface((1+a*cos(u))*cos(v),
                          (1+a*cos(u))*sin(v),a*sin(u),
                          (u,0,2*pi),(v,0,2*pi))
