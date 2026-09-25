import gradio as gr
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from rusle_soil_loss_estimator import compute_ls_factor, compute_annual_soil_loss

def erosion_risk_color_bar(soil_loss):
    """Return a simple colored bar emoji/text representation."""
    if soil_loss < 5:
        return "🟢 Low (<5 t/ha/yr) - Stable soil"
    elif soil_loss < 10:
        return "🟡 Moderate (5-10 t/ha/yr) - Tolerable loss"
    elif soil_loss < 20:
        return "🟠 High (10-20 t/ha/yr) - Active erosion"
    else:
        return "🔴 Severe (>20 t/ha/yr) - Critical erosion"

def make_factor_bar_chart(R, K, LS, C, P):
    """Produce a horizontal bar chart of factor magnitudes and return as PNG bytes."""
    factors = ["R", "K", "LS", "C", "P"]
    values = [R, K, LS, C, P]
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.barh(factors, values, color=['#2196F3','#4CAF50','#FF9800','#9C27B0','#795548'])
    ax.set_xlabel("Factor value")
    ax.set_title("RUSLE Factor Contributions")
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf

def calculate(R, K, LS_choice, slope_length, slope_steepness, C_dropdown, C_custom, P_dropdown, P_custom):
    """Main computation function triggered by 'Calculate' button."""
    # Validate R numeric
    try:
        R_val = float(R)
        if not (0 <= R_val <= 1000):
            return "R factor must be between 0 and 1000.", None, None
    except (ValueError, TypeError):
        return "Invalid R factor. Please enter a numeric value.", None, None

    # Validate K numeric
    try:
        K_val = float(K)
        if not (0 <= K_val <= 1):
            return "K factor must be between 0 and 1.", None, None
    except (ValueError, TypeError):
        return "Invalid K factor. Please enter a numeric value.", None, None

    # LS factor: either direct numeric or compute from slope
    LS_val = None
    if LS_choice == "Enter LS directly":
        try:
            LS_val = float(slope_length)  # we repurpose numeric input for LS
            if LS_val < 0:
                raise ValueError
        except (ValueError, TypeError):
            return "Invalid LS factor. Please enter a non-negative numeric value.", None, None
    else:  # compute from slope
        try:
            sl = float(slope_length)
            ss = float(slope_steepness)
            if sl <= 0 or ss < 0:
                raise ValueError
            LS_val = compute_ls_factor(sl, ss)
        except (ValueError, TypeError):
            return "Invalid slope length or steepness. Must be positive numbers.", None, None

    # C factor
    if C_dropdown == "Custom":
        try:
            C_val = float(C_custom)
            if not (0 <= C_val <= 1):
                raise ValueError
        except (ValueError, TypeError):
            return "Invalid C factor. Must be between 0 and 1.", None, None
    else:
        C_map = {"Bare soil 1.0": 1.0, "Row crops 0.5": 0.5, "Cereal crops 0.2": 0.2,
                 "Pasture 0.02": 0.02, "Forest 0.01": 0.01}
        C_val = C_map[C_dropdown]

    # P factor
    if P_dropdown == "Custom":
        try:
            P_val = float(P_custom)
            if not (0 <= P_val <= 1):
                raise ValueError
        except (ValueError, TypeError):
            return "Invalid P factor. Must be between 0 and 1.", None, None
    else:
        P_map = {"Straight row 1.0": 1.0, "Contour tillage 0.5": 0.5,
                 "Strip cropping 0.3": 0.3, "Terracing 0.2": 0.2}
        P_val = P_map[P_dropdown]

    # Compute soil loss
    A = compute_annual_soil_loss(R_val, K_val, LS_val, C_val, P_val)
    color_bar_text = erosion_risk_color_bar(A)
    summary = f"A = R × K × LS × C × P = {R_val:.1f} × {K_val:.3f} × {LS_val:.3f} × {C_val:.3f} × {P_val:.3f} = {A:.2f} t/ha/yr"
    # Factor chart
    chart_buf = make_factor_bar_chart(R_val, K_val, LS_val, C_val, P_val)
    return f"{A:.2f}", summary, chart_buf

# UI layout
with gr.Blocks(title="RUSLE Soil Loss Estimator", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🌍 RUSLE Soil Loss Estimator\n### Annual soil loss prediction using the Revised Universal Soil Loss Equation")
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Rainfall-Runoff (R) & Soil (K)")
            R_input = gr.Number(label="R factor (MJ mm ha⁻¹ h⁻¹ yr⁻¹)", value=100, minimum=0, maximum=1000, step=10)
            K_input = gr.Number(label="K factor (t ha h ha⁻¹ MJ⁻¹ mm⁻¹)", value=0.3, minimum=0, maximum=1, step=0.01)
            gr.Markdown("### Topographic (LS)")
            LS_choice = gr.Radio(["Enter LS directly", "Compute LS from slope"], label="LS input method", value="Compute LS from slope")
            with gr.Column(visible=True) as direct_ls_col:
                LS_direct = gr.Number(label="LS factor (dimensionless)", value=1.0, minimum=0, maximum=100, step=0.1)
            with gr.Column(visible=False) as compute_ls_col:
                slope_length = gr.Number(label="Slope length (m)", value=100, minimum=0.1, maximum=5000, step=1)
                slope_steepness = gr.Number(label="Slope steepness (%)", value=5, minimum=0, maximum=100, step=0.5)
            # Toggle visibility between direct and compute mode
            def toggle_ls_input(choice):
                if choice == "Enter LS directly":
                    return {direct_ls_col: gr.update(visible=True), compute_ls_col: gr.update(visible=False)}
                else:
                    return {direct_ls_col: gr.update(visible=False), compute_ls_col: gr.update(visible=True)}
            LS_choice.change(toggle_ls_input, inputs=LS_choice, outputs=[direct_ls_col, compute_ls_col])
            # For compute mode we reuse the slope_length field, but we also have slope_steepness
            # We'll handle in the calculate function by checking LS_choice value.
            # We need to pass all inputs. So we'll use slope_length as either LS (if direct) or length.
        with gr.Column(scale=1):
            gr.Markdown("### Cover (C) & Practice (P)")
            C_dropdown = gr.Dropdown(["Bare soil 1.0", "Row crops 0.5", "Cereal crops 0.2", "Pasture 0.02", "Forest 0.01", "Custom"], label="C factor", value="Pasture 0.02")
            C_custom = gr.Number(label="Custom C value", value=0.1, minimum=0, maximum=1, visible=False, step=0.01)
            def toggle_C_custom(choice):
                return {C_custom: gr.update(visible=(choice == "Custom"))}
            C_dropdown.change(toggle_C_custom, inputs=C_dropdown, outputs=C_custom)
            P_dropdown = gr.Dropdown(["Straight row 1.0", "Contour tillage 0.5", "Strip cropping 0.3", "Terracing 0.2", "Custom"], label="P factor", value="Contour tillage 0.5")
            P_custom = gr.Number(label="Custom P value", value=0.5, minimum=0, maximum=1, visible=False, step=0.01)
            def toggle_P_custom(choice):
                return {P_custom: gr.update(visible=(choice == "Custom"))}
            P_dropdown.change(toggle_P_custom, inputs=P_dropdown, outputs=P_custom)
            calc_btn = gr.Button("Calculate", variant="primary")
            gr.Markdown("### Results")
            soil_loss_output = gr.HTML(label="Annual Soil Loss (t/ha/yr)")
            summary_output = gr.Textbox(label="RUSLE Equation", interactive=False)
            chart_output = gr.Image(label="Factor Contributions", height=300)
            # Since calculate returns multiple outputs, we need to map them
            # We'll combine: first output string (A value with unit) passed to HTML
            # Actually we can return three values: a string for soil_loss_output (HTML), summary, chart
            # But soil_loss_output is HTML, so we need to pass HTML string.
            # Let's make calculate return three items: (A_html_str, summary_str, chart_bytes)
            # Then set outputs accordingly.
            def wrapped_calculate(R, K, LS_choice, slope_length, slope_steepness, C_dropdown, C_custom, P_dropdown, P_custom):
                A, summary, chart = calculate(R, K, LS_choice, slope_length, slope_steepness, C_dropdown, C_custom, P_dropdown, P_custom)
                if chart is None:  # error case, A is error string
                    return f"<div style='color:red;'><b>Error:</b> {A}</div>", summary, None
                else:
                    # Color-code the A value based on severity
                    if float(A) < 5:
                        color = "green"
                    elif float(A) < 10:
                        color = "#FFD700"
                    elif float(A) < 20:
                        color = "orange"
                    else:
                        color = "red"
                    html = f"<div style='font-size: 2em; font-weight: bold; color: {color};'>{A} t/ha/yr</div>"
                    # Add small bar below
                    risk_bar = f"<div style='height:10px; width:100%; background: linear-gradient(to right, green 25%, #FFD700 25% 50%, orange 50% 75%, red 75% 100%); border-radius:5px;'></div><p style='font-size:0.9em;'>{erosion_risk_color_bar(float(A))}</p>"
                    html += risk_bar
                    return html, summary, chart
            calc_btn.click(
                fn=wrapped_calculate,
                inputs=[R_input, K_input, LS_choice, slope_length, slope_steepness, C_dropdown, C_custom, P_dropdown, P_custom],
                outputs=[soil_loss_output, summary_output, chart_output]
            )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
