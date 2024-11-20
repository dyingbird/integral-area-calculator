import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify, Integral, latex, nsimplify, Piecewise, S
from sympy.core.sympify import SympifyError

# 제목 설정
st.title('함수 그래프와 넓이 계산기')

# 함수식 입력받기
func_input = st.text_input('함수식을 입력하세요 (예: sin(x), x**2 + 2*x + 1 등)')

# 적분 구간 입력받기 (수식으로 입력)
a_input = st.text_input('적분 시작 값 a를 입력하세요 (예: 0, pi/2 등)', value='0')
b_input = st.text_input('적분 끝 값 b를 입력하세요 (예: pi, 2*pi 등)', value='1')

if func_input and a_input and b_input:
    x = symbols('x')
    try:
        # 함수식을 SymPy 객체로 변환
        func_sympy = sympify(func_input)
        func_lambda = lambdify(x, func_sympy, modules=['numpy'])

        # 적분 구간을 SymPy 객체로 변환
        a_sympy = sympify(a_input)
        b_sympy = sympify(b_input)

        # 그래프 그리기 위한 x 값 생성 (실수 범위)
        a_float = float(a_sympy.evalf())
        b_float = float(b_sympy.evalf())
        x_vals = np.linspace(a_float, b_float, 400)
        y_vals = func_lambda(x_vals)

        # 그래프 설정
        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label=f'$y = {latex(func_sympy)}$')

        # 넓이 계산된 부분 색칠하기
        ax.fill_between(x_vals, 0, y_vals, where=(y_vals >= 0), color='skyblue', alpha=0.5, interpolate=True)
        ax.fill_between(x_vals, 0, y_vals, where=(y_vals <= 0), color='lightcoral', alpha=0.5, interpolate=True)

        # 축 설정
        ax.axhline(0, color='black', linewidth=0.5)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()

        # 그래프 출력
        st.pyplot(fig)

        # 양수 부분과 음수 부분 함수 정의
        func_positive = Piecewise((func_sympy, func_sympy >= 0), (0, True))
        func_negative = Piecewise((func_sympy, func_sympy <= 0), (0, True))

        # 양수 부분 넓이 계산
        area_positive = Integral(func_positive, (x, a_sympy, b_sympy)).doit()
        area_positive_simplified = nsimplify(area_positive, rational=True)
        area_positive_latex = latex(area_positive_simplified)

        # 음수 부분 넓이 계산 (절댓값 취함)
        area_negative = Integral(func_negative, (x, a_sympy, b_sympy)).doit()
        area_negative_simplified = nsimplify(-area_negative, rational=True)  # 음수이므로 부호 변경
        area_negative_latex = latex(area_negative_simplified)

        # 총 넓이 계산
        total_area = area_positive_simplified + area_negative_simplified
        total_area_latex = latex(total_area)

        # 결과 출력
        st.write('계산된 넓이:')
        st.latex(r'\displaystyle \text{양수 부분: } \int_{%s}^{%s} %s\,dx = %s' % (
            latex(a_sympy), latex(b_sympy), latex(func_positive), area_positive_latex))
        st.latex(r'\displaystyle \text{음수 부분: } \int_{%s}^{%s} %s\,dx = -%s' % (
            latex(a_sympy), latex(b_sympy), latex(func_negative), area_negative_latex))
        st.latex(r'\displaystyle \text{총 넓이: } %s + %s = %s' % (
            area_positive_latex, area_negative_latex, total_area_latex))

    except SympifyError:
        st.error('올바른 함수식과 적분 구간을 입력해주세요.')
    except Exception as e:
        st.error(f'오류가 발생했습니다: {e}')
