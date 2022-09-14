## Chatbot básico construido con tkinter y Transformers 🤗 En Español!!!

La carpeta contiene:

- `app.py` Archivo que corre la interfaz visual del chatbot
- `chat.py` Codigo para generar las respuestas del bot

Para el desarrollo se utilizaron los siguientes modelos pre-entrenados de HuggingFace 🤗

- `facebook/blenderbot-400M-distill` para generar un texto de respuesta por parte del Chatbot.
- Traductores: `Helsinki-NLP/opus-mt-en-es` de Inglés a Español y `Helsinki-NLP/opus-mt-es-en` de Español a Inglés.

Se uso el modelo `facebook/blenderbot-400M-distill`. [BlenderBot](https://ai.facebook.com/blog/state-of-the-art-open-source-chatbot/) fue desarrollado por Meta en 2020, con el fin de permitir una interacción más humana y natural.

El principio de funcionamiento es el siguiente:

- Se toma el texto de entrada, en español, generado por el usuario, se lo traduce al inglés y se pre-procesa usando un tokenizer
- La salida de este tokenizer se convertirá en la entrada de BlenderBot que logrará interpretar esta información y generar un texto de respuesta pero codificado en forma de tokens
- Se toman dichos tokens generados por BlenderBot y se los decodifica para obtener el texto de salida en inglés, el cual se traduce al español, convirtiendose en la respuesta que veremos en pantalla y con la cual podremos continuar la interacción.

En todo momento se trabajó con modelos disponibles pre-entrenados. Lo cual lleva a que la interaccion pueda tener algunos errores. Puede decirse que esta es una versión de pruba 🙂 
