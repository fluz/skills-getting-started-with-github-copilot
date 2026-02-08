document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        // Create activity card structure using DOM APIs
        const h4 = document.createElement("h4");
        h4.textContent = name;
        
        const descP = document.createElement("p");
        descP.textContent = details.description;
        
        const scheduleP = document.createElement("p");
        const scheduleStrong = document.createElement("strong");
        scheduleStrong.textContent = "Schedule: ";
        scheduleP.appendChild(scheduleStrong);
        scheduleP.appendChild(document.createTextNode(details.schedule));
        
        const availabilityP = document.createElement("p");
        const availabilityStrong = document.createElement("strong");
        availabilityStrong.textContent = "Availability: ";
        availabilityP.appendChild(availabilityStrong);
        availabilityP.appendChild(document.createTextNode(`${spotsLeft} spots left`));
        
        const participantsDiv = document.createElement("div");
        participantsDiv.className = "participants";
        const participantsStrong = document.createElement("strong");
        participantsStrong.textContent = "Participants:";
        participantsDiv.appendChild(participantsStrong);
        
        const participantsList = document.createElement("ul");
        
        if (details.participants.length === 0) {
          const noParticipantsLi = document.createElement("li");
          noParticipantsLi.textContent = "No participants yet";
          participantsList.appendChild(noParticipantsLi);
        } else {
          details.participants.forEach((participant) => {
            const li = document.createElement("li");
            // Use textContent to safely display participant email
            li.appendChild(document.createTextNode(participant));
            li.appendChild(document.createTextNode(" "));
            
            const deleteButton = document.createElement("button");
            deleteButton.className = "delete-participant";
            // Use setAttribute to safely set data attributes
            deleteButton.setAttribute("data-email", participant);
            deleteButton.setAttribute("data-activity", name);
            deleteButton.textContent = "Delete";
            
            li.appendChild(deleteButton);
            participantsList.appendChild(li);
          });
        }
        
        participantsDiv.appendChild(participantsList);
        
        activityCard.appendChild(h4);
        activityCard.appendChild(descP);
        activityCard.appendChild(scheduleP);
        activityCard.appendChild(availabilityP);
        activityCard.appendChild(participantsDiv);
        
        activitiesList.appendChild(activityCard);
        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });

      // Reapply delete functionality after rendering
      addDeleteFunctionality();
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        fetchActivities(); // Refresh the activities list automatically
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Add delete functionality
  function addDeleteFunctionality() {
    const deleteButtons = document.querySelectorAll(".delete-participant");

    deleteButtons.forEach((button) => {
      button.addEventListener("click", async (event) => {
        const participantEmail = event.target.dataset.email;
        const activityName = event.target.dataset.activity;

        try {
          const response = await fetch(
            `/activities/${encodeURIComponent(activityName)}/unregister?email=${encodeURIComponent(participantEmail)}`,
            {
              method: "DELETE",
            }
          );

          if (response.ok) {
            fetchActivities(); // Refresh the activities list
          } else {
            console.error("Failed to unregister participant");
          }
        } catch (error) {
          console.error("Error unregistering participant:", error);
        }
      });
    });
  }

  // Initialize app
  fetchActivities().then(() => {
    addDeleteFunctionality();
  });
});
