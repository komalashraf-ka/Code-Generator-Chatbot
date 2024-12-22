
        const templates = {
            python: `# Python Template\nprint("Hello, World!")`,
            r: `# R Template\nprint("Hello, World!")`,
            html: `<!-- HTML Template -->\n<div>Hello, World!</div>`,
            css: `/* CSS Template */\nbody {\n    background-color: lightblue;\n}`,
            javascript: `// JavaScript Template\nconsole.log("Hello, World!");`
        };

        const setTemplate = (language) => {
            const codeDisplay = document.getElementById('code-display');
            codeDisplay.textContent = templates[language] || "// No template available for this language.";
        };

        const sendButton = document.getElementById("send-button");
        const consoleInput = document.getElementById("console-input");
        const consoleOutput = document.getElementById("console-output");


        sendButton.addEventListener("click", async () => {
            const prompt = consoleInput.value.trim();
            if (prompt) {
                consoleOutput.textContent += `\n> ${prompt}`;
                consoleInput.value = ""; 

                try {
                    const response = await fetch('/generate_code', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ prompt })
                    });
                    const data = await response.json();
                    if (data.code) {
                        document.getElementById('code-display').textContent = data.code;
                    } else {
                        consoleOutput.textContent += `\nError: ${data.error}`;
                    }
                } catch (error) {
                    consoleOutput.textContent += `\nError: ${error.message}`;
                }
            }
        });
