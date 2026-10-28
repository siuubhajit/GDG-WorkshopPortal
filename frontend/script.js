const CLOUD_FUNCTION_URL = "YOURCLOUD_FUNCTION_URL_HERE";

document.getElementById('registrationForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const submitBtn = document.getElementById('submitBtn');
  const message = document.getElementById('responseMessage');

  const payload = {
    name: document.getElementById('name').value,
    email: document.getElementById('email').value,
    department: document.getElementById('department').value,
    interest: document.getElementById('interest').value
  };

  submitBtn.disabled = true;
  message.textContent = "Submitting...";

  try {
    const res = await fetch(CLOUD_FUNCTION_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (res.ok) {
      message.style.color = "green";
      message.textContent = data.message || "Submitted successfully!";
      document.getElementById('registrationForm').reset();
    } else {
      throw new Error(data.error || "Submission failed.");
    }
  } catch (err) {
    message.style.color = "red";
    message.textContent = err.message;
  } finally {
    submitBtn.disabled = false;
  }
});
