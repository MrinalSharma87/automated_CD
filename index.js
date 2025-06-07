document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("analyze-button").addEventListener("click", async function () {
      const file1 = document.getElementById("file1").files[0];
      const file2 = document.getElementById("file2").files[0];

      if (!file1 || !file2) {
        alert("Please upload both files.");
        return;
      }

      const formData = new FormData();
      formData.append("file1", file1);
      formData.append("file2", file2);

      const loading = document.getElementById("loading");
      const resultsDiv = document.getElementById("results");
      resultsDiv.innerHTML = "";
      loading.style.display = "block";

      try {
        const response = await fetch("http://127.0.0.1:5000/analyze", {
          method: "POST",
          body: formData
        });

        if (!response.ok) throw new Error("Network response was not ok");

        const data = await response.json();
        loading.style.display = "none";

        if (data.length === 0) {
          resultsDiv.innerHTML = "<p>No significant changes detected.</p>";
          return;
        }

        data.forEach(change => {
          const card = document.createElement("div");
          card.className = "result-card";

          card.innerHTML = `
            <div class="summary">🔄 ${change.change_summary}</div>
            <div class="detail"><strong>Type:</strong> ${change.change_type}</div>
            <div class="detail"><strong>Impact:</strong> ${change.potential_impact}</div>
          `;

          resultsDiv.appendChild(card);
        });

      } catch (error) {
        loading.style.display = "none";
        alert("Error occurred: " + error.message);
        console.error(error);
      }
    });
  });