const cityInput = document.getElementById("city");
const weatherForm = document.getElementById("weather-form")
const result = document.getElementById("result");

weatherForm.addEventListener("submit", async function (event) {
  event.preventDefault();
  const city = cityInput.value.trim();

  if (!city) {
        result.textContent = "Please enter a city name.";
        return;
    }result.textContent = "Loading...";

    try {
       
        const response = await fetch(`/weather?city=${encodeURIComponent(city)}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to get weather data.");
        }

        result.innerHTML = `
            <h2>Weather in ${(data.name)}, ${(data.sys.country)}</h2>
            <p>Temperature: ${data.main.temp} °C</p>
            <p>Feels like: ${data.main.feels_like} °C</p>
            <p>Humidity: ${data.main.humidity}%</p>
            <p>Weather: ${(data.weather[0].description)}</p>
        `;
    } catch (error) {
        result.textContent = error.message;
    }
});


function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value ?? "";
    return div.innerHTML;
}
