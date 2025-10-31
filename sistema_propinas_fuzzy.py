import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import os

output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"✓ Carpeta '{output_dir}/' creada\n")

print("=" * 60)
print("Sistema de Decisión de Propinas usando Lógica Difusa")
print("=" * 60)

calidad_servicio = ctrl.Antecedent(np.arange(0, 11, 1), 'calidad_servicio')
calidad_comida = ctrl.Antecedent(np.arange(0, 11, 1), 'calidad_comida')
propina = ctrl.Consequent(np.arange(0, 26, 1), 'propina')

calidad_servicio['mala'] = fuzz.trimf(calidad_servicio.universe, [0, 0, 5])
calidad_servicio['aceptable'] = fuzz.trimf(calidad_servicio.universe, [0, 5, 10])
calidad_servicio['excelente'] = fuzz.trimf(calidad_servicio.universe, [5, 10, 10])

calidad_comida['mala'] = fuzz.trimf(calidad_comida.universe, [0, 0, 5])
calidad_comida['aceptable'] = fuzz.trimf(calidad_comida.universe, [0, 5, 10])
calidad_comida['excelente'] = fuzz.trimf(calidad_comida.universe, [5, 10, 10])

propina['baja'] = fuzz.trimf(propina.universe, [0, 0, 13])
propina['media'] = fuzz.trimf(propina.universe, [0, 13, 25])
propina['alta'] = fuzz.trimf(propina.universe, [13, 25, 25])

regla1 = ctrl.Rule(calidad_servicio['mala'] | calidad_comida['mala'], propina['baja'])
regla2 = ctrl.Rule(calidad_servicio['aceptable'], propina['media'])
regla3 = ctrl.Rule(calidad_servicio['excelente'] | calidad_comida['excelente'], propina['alta'])

sistema_propinas_ctrl = ctrl.ControlSystem([regla1, regla2, regla3])
sistema_propinas = ctrl.ControlSystemSimulation(sistema_propinas_ctrl)

print("\n--- Visualización de Funciones de Pertenencia ---\n")

fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

calidad_servicio.view(ax=ax0)
ax0.set_title('Funciones de Pertenencia - Calidad del Servicio')
ax0.legend(loc='upper right')

calidad_comida.view(ax=ax1)
ax1.set_title('Funciones de Pertenencia - Calidad de la Comida')
ax1.legend(loc='upper right')

propina.view(ax=ax2)
ax2.set_title('Funciones de Pertenencia - Propina (%)')
ax2.legend(loc='upper right')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'funciones_pertenencia.png'), dpi=300, bbox_inches='tight')
print(f"✓ Gráfico de funciones de pertenencia guardado: {output_dir}/funciones_pertenencia.png")

print("\n--- Evaluación de Casos de Ejemplo ---\n")

casos_prueba = [
    {"servicio": 3, "comida": 8, "descripcion": "Servicio malo, comida excelente"},
    {"servicio": 6.5, "comida": 6, "descripcion": "Servicio y comida aceptables"},
    {"servicio": 9, "comida": 9.5, "descripcion": "Servicio y comida excelentes"},
    {"servicio": 2, "comida": 3, "descripcion": "Servicio y comida malos"}
]

resultados = []

for i, caso in enumerate(casos_prueba, 1):
    sistema_propinas.input['calidad_servicio'] = caso['servicio']
    sistema_propinas.input['calidad_comida'] = caso['comida']

    sistema_propinas.compute()

    propina_resultado = sistema_propinas.output['propina']

    print(f"Caso {i}: {caso['descripcion']}")
    print(f"  Servicio: {caso['servicio']}/10")
    print(f"  Comida: {caso['comida']}/10")
    print(f"  → Propina sugerida: {propina_resultado:.2f}%")
    print()

    resultados.append({
        'caso': i,
        'servicio': caso['servicio'],
        'comida': caso['comida'],
        'propina': propina_resultado,
        'descripcion': caso['descripcion']
    })

print("\n--- Visualización de un Caso Específico ---\n")

sistema_propinas.input['calidad_servicio'] = 6.5
sistema_propinas.input['calidad_comida'] = 9.5

sistema_propinas.compute()

fig, ax = plt.subplots(figsize=(10, 5))
propina.view(sim=sistema_propinas, ax=ax)
ax.set_title('Resultado del Sistema Fuzzy\n(Servicio: 6.5, Comida: 9.5)')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'resultado_ejemplo.png'), dpi=300, bbox_inches='tight')
print(f"✓ Gráfico de resultado específico guardado: {output_dir}/resultado_ejemplo.png")

print("\n--- Superficie de Control 3D ---\n")

servicio_range = np.arange(0, 11, 0.5)
comida_range = np.arange(0, 11, 0.5)
propina_surface = np.zeros((len(servicio_range), len(comida_range)))

for i, servicio_val in enumerate(servicio_range):
    for j, comida_val in enumerate(comida_range):
        sistema_propinas.input['calidad_servicio'] = servicio_val
        sistema_propinas.input['calidad_comida'] = comida_val
        sistema_propinas.compute()
        propina_surface[i, j] = sistema_propinas.output['propina']

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

servicio_mesh, comida_mesh = np.meshgrid(comida_range, servicio_range)
surf = ax.plot_surface(servicio_mesh, comida_mesh, propina_surface,
                       cmap='viridis', alpha=0.8, edgecolor='none')

ax.set_xlabel('Calidad de la Comida')
ax.set_ylabel('Calidad del Servicio')
ax.set_zlabel('Propina (%)')
ax.set_title('Superficie de Control del Sistema Fuzzy')

fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

plt.savefig(os.path.join(output_dir, 'superficie_control_3d.png'), dpi=300, bbox_inches='tight')
print(f"✓ Gráfico de superficie 3D guardado: {output_dir}/superficie_control_3d.png")

print("\n--- Análisis de Sensibilidad ---\n")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

comida_fija = 7
servicio_vals = np.arange(0, 11, 0.2)
propina_vals = []

for servicio_val in servicio_vals:
    sistema_propinas.input['calidad_servicio'] = servicio_val
    sistema_propinas.input['calidad_comida'] = comida_fija
    sistema_propinas.compute()
    propina_vals.append(sistema_propinas.output['propina'])

ax1.plot(servicio_vals, propina_vals, 'b-', linewidth=2)
ax1.set_xlabel('Calidad del Servicio')
ax1.set_ylabel('Propina (%)')
ax1.set_title(f'Propina vs Servicio (Comida fija = {comida_fija})')
ax1.grid(True, alpha=0.3)

servicio_fijo = 7
comida_vals = np.arange(0, 11, 0.2)
propina_vals2 = []

for comida_val in comida_vals:
    sistema_propinas.input['calidad_servicio'] = servicio_fijo
    sistema_propinas.input['calidad_comida'] = comida_val
    sistema_propinas.compute()
    propina_vals2.append(sistema_propinas.output['propina'])

ax2.plot(comida_vals, propina_vals2, 'r-', linewidth=2)
ax2.set_xlabel('Calidad de la Comida')
ax2.set_ylabel('Propina (%)')
ax2.set_title(f'Propina vs Comida (Servicio fijo = {servicio_fijo})')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'analisis_sensibilidad.png'), dpi=300, bbox_inches='tight')
print(f"✓ Gráfico de análisis de sensibilidad guardado: {output_dir}/analisis_sensibilidad.png")

print("\n" + "=" * 60)
print("Ejecución completada exitosamente")
print("=" * 60)
print(f"\nArchivos generados en la carpeta '{output_dir}/':")
print("  1. funciones_pertenencia.png - Funciones de membresía")
print("  2. resultado_ejemplo.png - Ejemplo de inferencia")
print("  3. superficie_control_3d.png - Superficie 3D del sistema")
print("  4. analisis_sensibilidad.png - Análisis de sensibilidad")
print("\n")
