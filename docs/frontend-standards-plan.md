# Plan de acción: estándares para la creación del frontend

## Objetivo

Definir un marco de trabajo para que el futuro frontend sea consistente,
accesible, mantenible y fácil de validar, sin imponer una librería o una
implementación técnica concreta al desarrollador que lo construya.

El frontend será la interfaz principal del proyecto y consumirá el backend
Django mediante la API HTTP existente. El CLI se mantendrá fuera del flujo de
usuario.

## Alcance

Incluye:

- Criterios de producto y experiencia de usuario.
- Reglas visuales y de interacción.
- Accesibilidad y diseño responsive.
- Integración con la API y gestión de estados.
- Calidad, pruebas, seguridad y observabilidad.
- Criterios de aceptación y entrega.

No incluye:

- Implementación de componentes o pantallas.
- Elección obligatoria de framework, librería visual o gestor de estado.
- Rediseño del backend.
- Autenticación de usuarios, tiempo real o funcionalidades no expuestas por
  la API actual.

## Fases propuestas

### 1. Alinear el producto antes de desarrollar

- Definir el flujo principal: configurar una ladder, generarla, revisar el
  resultado y consultar el historial.
- Identificar los estados que deben existir en cada pantalla: inicial,
  cargando, éxito, vacío, validación y error.
- Acordar el vocabulario visible para el usuario y mantenerlo consistente.
- Definir qué información es imprescindible y qué información es secundaria.
- Establecer qué comportamientos quedan fuera de la primera versión.

### 2. Establecer una base visual coherente

- Crear una guía breve de colores, tipografía, espaciado, bordes, sombras e
  iconografía.
- Definir componentes reutilizables para botones, campos, alertas, tablas,
  tarjetas, paginación y estados vacíos.
- Evitar estilos aislados o duplicados por pantalla.
- Mantener una jerarquía visual clara: acción principal, resultado y acciones
  secundarias.
- Diseñar primero para claridad y legibilidad, no para añadir elementos
  decorativos.

### 3. Diseñar la experiencia responsive y accesible

- La aplicación debe funcionar en móvil, tablet y escritorio.
- Los formularios deben ser utilizables con teclado y lectores de pantalla.
- Cada campo debe tener etiqueta visible, ayuda contextual cuando sea
  necesaria y mensajes de error asociados.
- No depender únicamente del color para comunicar estados.
- Mantener contraste suficiente, foco visible y objetivos táctiles cómodos.
- Respetar las preferencias de reducción de movimiento cuando existan
  animaciones.
- Definir un orden lógico de navegación por teclado.

### 4. Integrar el frontend con el contrato backend

- Centralizar las llamadas HTTP en una única capa de cliente.
- Respetar los formatos y códigos de respuesta documentados por la API.
- Inicializar CSRF antes de cualquier operación mutante.
- Enviar credenciales para conservar la sesión anónima y el historial.
- No duplicar en el frontend la lógica de selección o generación de ladders.
- Mostrar errores de validación, ausencia de niveles y fallos de AREDL de
  forma comprensible.
- Tratar el historial como información de la sesión actual, sin prometer
  autenticación ni sincronización entre dispositivos.

### 5. Gestionar estados y errores de forma explícita

- Cada operación asíncrona debe tener estados de carga, éxito, error y
  reintento cuando aplique.
- Desactivar o proteger las acciones mientras una generación está en curso para
  evitar envíos duplicados.
- Mantener los datos introducidos por el usuario cuando una petición falla.
- Proporcionar mensajes accionables, evitando mostrar trazas técnicas.
- Distinguir entre errores de entrada, errores temporales y errores del
  servidor.
- Mostrar correctamente resultados vacíos y ladders con advertencias.

### 6. Mantener calidad de código

- Separar presentación, estado de pantalla, cliente API y modelos de datos.
- Usar nombres consistentes y componentes pequeños con una responsabilidad
  clara.
- Evitar duplicación de reglas, textos y estilos.
- Mantener el contrato de datos tipado o validado en los límites de la
  aplicación.
- Documentar únicamente decisiones no obvias o restricciones de negocio.
- No introducir dependencias sin justificar su beneficio y mantenimiento.

### 7. Definir una estrategia mínima de pruebas

- Pruebas de componentes para formularios, validaciones, estados vacíos y
  mensajes de error.
- Pruebas de integración para generación, CSRF, sesión e historial.
- Pruebas de navegación para el flujo principal de usuario.
- Comprobaciones responsive en tamaños representativos.
- Comprobaciones de teclado y accesibilidad antes de cada entrega.
- Verificación de que una respuesta inesperada del backend no rompe la
  interfaz.

### 8. Aplicar seguridad y privacidad desde el inicio

- No incluir secretos, tokens ni credenciales en el código del frontend.
- Mantener el uso de CSRF y cookies de sesión según el contrato Django.
- No registrar en consola datos sensibles o información innecesaria de sesión.
- Validar entradas en la interfaz sin sustituir la validación del backend.
- Evitar HTML insertado directamente salvo que exista una necesidad revisada.
- Revisar dependencias y mantenerlas actualizadas.

### 9. Establecer criterios de entrega

Una funcionalidad se considerará lista cuando:

- Cumpla el flujo funcional acordado.
- Funcione en móvil y escritorio.
- Tenga estados de carga, éxito, vacío y error.
- Sea navegable por teclado y tenga etiquetas accesibles.
- Respete el contrato de la API y la sesión anónima.
- Incluya pruebas apropiadas.
- No deje errores de consola ni advertencias conocidas sin documentar.
- Haya sido revisada visualmente en los navegadores objetivo.
- Incluya una descripción breve de cambios, decisiones y limitaciones.

### 10. Evolucionar sin bloquear la primera versión

- Priorizar primero generación, visualización de resultados e historial.
- Mantener autenticación, preferencias persistentes, tiempo real y
  funcionalidades avanzadas fuera de la primera entrega salvo nueva decisión.
- Recoger feedback sobre claridad, errores y utilidad antes de ampliar el
  alcance.
- Revisar periódicamente el contrato API y la guía visual cuando aparezcan
  nuevas necesidades.

## Resultado esperado

Al finalizar este plan debe existir una primera versión web que:

- Sea clara para un usuario que no conoce el CLI.
- Permita completar el flujo principal sin conocimientos técnicos.
- Comunique todos los estados importantes.
- Sea usable con teclado, móvil y lectores de pantalla.
- Mantenga una separación clara entre interfaz y lógica del backend.
- Pueda evolucionar sin rehacer cada pantalla ni duplicar reglas.
