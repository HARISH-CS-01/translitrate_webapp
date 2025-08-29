document.addEventListener("DOMContentLoaded", () => {
    const inputText = document.getElementById("inputText");
    const outputDiv = document.getElementById("output");
    const translateBtn = document.getElementById("translateBtn");
  
    translateBtn.addEventListener("click", async () => {
      const text = inputText.value.trim();
  
      if (!text) {
        outputDiv.textContent = "⚠️ Please enter some text first.";
        return;
      }
  
      outputDiv.textContent = "⏳ Transliteration in progress...";
  
      try {
        const response = await fetch("/transliterate", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ text })
        });
  
        const data = await response.json();
  
        if (data.output) {
          outputDiv.style.opacity = 0;
          outputDiv.textContent = data.output;
  
          setTimeout(() => {
            outputDiv.style.transition = "opacity 0.6s";
            outputDiv.style.opacity = 1;
          }, 50);
        } else {
          outputDiv.textContent = "⚠️ No output received from server.";
        }
      } catch (err) {
        console.error("Error:", err);
        outputDiv.textContent = "❌ Error while transliterating.";
      }
    });
  });
  