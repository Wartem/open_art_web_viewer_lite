function initializeSearch(config) {
    const { resultsContainer, loadMoreButton, loadingIndicator, modal, modalImage, modalTitle, downloadLink, fallbackImageUrl } = config;
    
    const total = parseInt(resultsContainer.dataset.total);
    const perPage = parseInt(resultsContainer.dataset.perPage);
    let currentPage = parseInt(resultsContainer.dataset.currentPage);
    const query = resultsContainer.dataset.query;
    const searchType = resultsContainer.dataset.searchType;
    const artType = resultsContainer.dataset.artType;
  
    let loading = false;
    let hasMore = total > currentPage * perPage;
  
    function debounce(func, wait) {
      let timeout;
      return function executedFunction(...args) {
        const later = () => {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    }
  
    function loadMoreResults() {
      if (loading || !hasMore) return;
      loading = true;
      loadingIndicator.hidden = false;
  
      fetch(`/api/search?query=${query}&page=${currentPage + 1}&search_type=${searchType}&art_type=${artType}`)
        .then(response => response.json())
        .then(data => {
          appendResults(data.results);
          currentPage++;
          hasMore = data.has_more;
          loading = false;
          loadingIndicator.hidden = true;
          loadMoreButton.hidden = !hasMore;
        })
        .catch(error => {
          console.error("Error fetching more results:", error);
          loading = false;
          loadingIndicator.hidden = true;
          alert("An error occurred while loading more results. Please try again.");
        });
    }
  
    function appendResults(results) {
      results.forEach((artwork, index) => {
        setTimeout(() => {
          const div = document.createElement("div");
          div.className = "col-sm-6 col-md-4 col-lg-3 artwork-card";
          div.innerHTML = `
            <div class="card h-100">
              <div class="zoom-container" style="height: 200px;">
                <img class="card-img-top zoom-image" src="${artwork.imgurl_thumb}" alt="${artwork.title}" 
                     style="height: 100%; width: 100%;" loading="lazy">
              </div>
              <div class="card-body">
                <h3 class="card-title">${artwork.title}</h3>
                <dl class="artwork-info">
                  <dt>Source:</dt><dd>${artwork.source}</dd>
                  <dt>Attribution:</dt><dd>${artwork.attribution}</dd>
                  <dt>Created:</dt><dd>${artwork.displaydate}</dd>
                  <dt>Display date:</dt><dd>${artwork.displaydate} (${artwork.beginyear} - ${artwork.endyear})</dd>
                  <dt>Classification:</dt><dd>${artwork.classification}</dd>
                  <dt>Medium:</dt><dd>${artwork.medium}</dd>
                  <dt>Dimensions:</dt><dd>${artwork.width} x ${artwork.height}</dd>
                </dl>
              </div>
            </div>
          `;
  
          const img = div.querySelector(".card-img-top");
          img.onerror = () => {
            img.src = fallbackImageUrl;
            img.alt = "Image not available";
          };
  
          if (img.src !== fallbackImageUrl) {
            img.addEventListener("click", () => openModal(artwork));
            img.style.cursor = "pointer";
          }
  
          resultsContainer.appendChild(div);
        }, index * 50);
      });
    }
  
    function openModal(artwork) {
      modalImage.src = artwork.imgurl_downsized;
      modalImage.alt = artwork.title;
      modalTitle.textContent = `${artwork.title} by ${artwork.attribution}`;
      downloadLink.href = artwork.imgurl_full;
      downloadLink.download = `${artwork.title.replace(/[^a-z0-9]/gi, "_")}_full.jpg`;
      modal.setAttribute('aria-hidden', 'false');
      modal.style.display = "block";
    }
  
    function closeModal() {
      modal.setAttribute('aria-hidden', 'true');
      modal.style.display = "none";
    }
  
    // Event Listeners
    loadMoreButton.addEventListener("click", loadMoreResults);
    window.addEventListener("scroll", debounce(() => {
      if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 500) {
        loadMoreResults();
      }
    }, 250));
  
    modal.querySelector(".close").addEventListener("click", closeModal);
    window.addEventListener("click", (event) => {
      if (event.target == modal) {
        closeModal();
      }
    });
  
    // Initial load
    if (total > 0) {
      loadMoreResults();
    } else {
      resultsContainer.innerHTML = "<p class='text-center'>No results found.</p>";
    }
  }

  function handleMouseOver(event) {
    const targetElement = event.target;
    if (
      targetElement.classList.contains("card-img-top") &&
      targetElement.src !== fallbackImageUrl
    ) {
      if (currentHoveredImage === targetElement) return; // Don't trigger hover effect again
      currentHoveredImage = targetElement;
      // Trigger hover effect here...
    }
  }

      function parseAndFixJson(jsonString) {
        // Step 1: Try parsing the original string without cleaning
        try {
          return JSON.parse(jsonString);
        } catch (error) {
          console.log(
            "Failed to parse original string. Attempting to fix and clean..."
          );
          // Remove the return [] statement to allow the function to continue
        }
      
        // Step 2: If parsing fails, use an advanced fix method
        function advancedFixJsonString(str) {
          // Remove any leading/trailing whitespace
          str = str.trim();
      
          // Replace single quotes with double quotes if any
          str = str.replace(/'/g, '"');
      
          // Ensure the string starts and ends with appropriate brackets
          if (!str.startsWith("[") && !str.startsWith("{")) str = "[" + str;
          if (!str.endsWith("]") && !str.endsWith("}")) str = str + "]";
      
          // Replace any unescaped newlines, tabs, and carriage returns
          str = str
            .replace(/(?<!\\)\n/g, "\\n")
            .replace(/(?<!\\)\r/g, "\\r")
            .replace(/(?<!\\)\t/g, "\\t");
      
          // Fix common JSON syntax errors
          str = str.replace(/,\s*]/g, "]"); // Remove trailing commas in arrays
          str = str.replace(/,\s*}/g, "}"); // Remove trailing commas in objects
      
          // Debugging: Log the fixed string
          console.log("Fixed JSON String:", str);
      
          return str;
        }
      
        // Step 3: Try parsing the fixed and cleaned string
        try {
          let fixedString = advancedFixJsonString(jsonString);
          return JSON.parse(fixedString);
        } catch (error) {
          console.log(
            "Failed to parse fixed string. Replacing with error text..."
          );
        }
      
        // Step 4: If all else fails, return a JSON object with error information
        return {
          error: true,
          message: "Failed to parse JSON",
          originalString: jsonString.substring(0, 500) + "...", // Increase to first 500 characters for better context
        };
      }

      const resultsContainer = document.getElementById("results-container");
      const {
        total,
        perPage,
        currentPage: currentPageData,
        query,
        searchType,
        artType,
        projectName
      } = resultsContainer.dataset;
      let currentPage = parseInt(currentPageData);
      
      let currentHoveredImage = null;
      const fallbackImageUrl = "{{ url_for('static', filename='images/image_not_found.jpg') }}";
      let loading = false;
      
      const hasMore = () => parseInt(total) > currentPage * parseInt(perPage);
      
      // Initial Load
      document.addEventListener('DOMContentLoaded', () => {
        const initialResultsString = '{{ results|tojson|safe }}';
        const parsedJson = parseAndFixJson(initialResultsString);
      
        if (parsedJson?.length > 0) {
          appendResults(parsedJson);
          document.getElementById("load-more").style.display = hasMore() ? "block" : "none";
        } else if (parseInt(total) > 0) {
          loadMoreResults();
        } else {
          resultsContainer.innerHTML = "<p class='text-center'>No results found.</p>";
        }
      });
      
      // Infinite Scroll with Debounce
      window.addEventListener(
        "scroll",
        debounce(() => {
          if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 500) {
            loadMoreResults();
          }
        }, 250)
      );
      
      // Load More Button Click Event
      document.getElementById("load-more").addEventListener("click", loadMoreResults);
      
      document.addEventListener('mouseover', handleMouseOver);
  
      