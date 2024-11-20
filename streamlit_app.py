import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify, Integral, latex
from sympy.core.sympify import SympifyError

# 제목 설정
st.title('함수 그래프와 넓이 계산기')

# 함수식 입력받기
func_input = st.text_input('함수식을 입력하세요 (예: sin(x), x**2 + 2*x + 1 등)')

# 적분 구간 입력받기
a = st.number_input('적분 시작 값 a를 입력하세요', value=0.0)
b = st.number_input('적분 끝 값 b를 입력하세요', value=1.0)

if func_input:
    x = symbols('x')
    try:
        # 함수식을 SymPy 객체로 변환
        func_sympy = sympify(func_input)
        func_lambda = lambdify(x, func_sympy, modules=['numpy'])
        
        # 그래프 그리기 위한 x 값 생성
        x_vals = np.linspace(float(a), float(b), 400)
        y_vals = func_lambda(x_vals)
        
        # 그래프 설정
        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label=f'$y = {latex(func_sympy)}$')
        
        # 넓이 계산된 부분 색칠하기
        ax.fill_between(x_vals, y_vals, where=(y_vals>=0), color='skyblue', alpha=0.5, interpolate=True)
        ax.fill_between(x_vals, y_vals, where=(y_vals<=0), color='lightcoral', alpha=0.5, interpolate=True)
        
        # 축 설정
        ax.axhline(0, color='black', linewidth=0.5)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()
        
        # 그래프 출력
        st.pyplot(fig)
        
        # 넓이 계산
        area = Integral(func_sympy, (x, a, b)).doit()
        area_latex = latex(area)
        
        # 결과 출력
        st.markdown(f'계산된 넓이: $\\int_{{{a}}}^{{{b}}} {latex(func_sympy)}\\,dx = {area_latex}$')
        
    except SympifyError:
        st.error('올바른 함수식을 입력해주세요.')
    except Exception as e:
        st.error(f'오류가 발생했습니다: {e}')
