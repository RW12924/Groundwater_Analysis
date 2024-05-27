function generateSiteData(selectedStation) {
  d3.json("https://data.cnra.ca.gov/api/3/action/datastore_search?resource_id=af157380-fb42-4abf-b72a-6f9f98868077&limit=47000")
    .then((data) => {
      var siteData = data.result.records;

      // Filter the data for the object with the selected station / site code
      var filteredSiteData = siteData.filter(obj => obj.site_code == selectedStation)[0];

      // Selects the panel with id of `#site-data`
      var panel = d3.select('#site-data');

      // Clears any existing site data
      panel.html("");

      // Sets paragraph and column parameters for formatting
      var paragraphCounter = 0;
      var columnCounter = 1;

      Object.entries(filteredSiteData).forEach(([key, value]) => {
        // Starts a new column after the 10th paragraph
        if (paragraphCounter % 10 === 0) {
          columnDiv = panel.append('div').classed('col-md-6', true);
          columnCounter++;
        }
        // Appends paragraph to the current column div
        columnDiv.append('p').text(`${key}: ${value}`);
        paragraphCounter++;
      });
    })
}
  
// Function to generate line chart
function generateLineChart(filteredResults, startDate, endDate) {

    // Filter dates based on the selected start and end dates
    var filteredDates = filteredResults.filter(date => {
    var dateObj = new Date(date.msmt_date);
    return dateObj >= startDate && dateObj <= endDate;
    });

    // Gets the msmt_date and gwe values
    var msmtDate = filteredDates.map(date => date.msmt_date);
    var gweValues = filteredDates.map(date => date.gwe);

    // Builds the line chart
    var lineTrace = {
    'x': msmtDate,
    'y': gweValues,
    'mode': 'lines+markers',
    'type': 'scatter',
    'name': 'GWE',
    'line': { width: 3, connectgaps: true },
    'marker': { size: 7 }
    };

    var lineData = [lineTrace];

    var lineLayout = {
    'title': 'Change in Groundwater Elevation Over Time',
    'xaxis': {'title': 'Dates'},
    'yaxis': {'title': 'GWE (ft)'}
    };

    // Renders the line chart
    Plotly.newPlot('scatter', lineData, lineLayout);

}

// Function to generate histogram
function generateHistogram(filteredResults, selectedStation) {

  // Gets the gwe values
  var histGweValues = filteredResults.map(date => date.gwe);

  // Builds the histogram
  var histogramTrace = {
    'x': histGweValues,
    'type': 'histogram',
    'name': 'GWE',
  };

  var histogramData = [histogramTrace];

  var histogramLayout = {
    'title': `All Groundwater Elevation Measurements for Site Code`,
    'xaxis': {'title': 'GWE (ft)'},
    'yaxis': {'title': 'Count'}
  };

  // Renders the histogram
  Plotly.newPlot('histogram', histogramData, histogramLayout);
}

// Function to generate statistical data
function generateStatsData(filteredResults){

  // Gets the gwe values
  var statsGweValues = filteredResults.map(obj => obj.gwe);

  // Calculates the statistics
  var gweMax = Math.max(...statsGweValues);
  var gweMin = Math.min(...statsGweValues);
  var gweMedian = calculateMedian(statsGweValues);
  var gweAvg = calculateAverage(statsGweValues);

  // Displays the statistics panel
  var statsPanel= d3.select('#stats-panel');
  statsPanel.html(
    `<p><strong>All-Time High GWE:</strong> ${gweMax} feet</p>` +
    `<p><strong>All-Time Low GWE:</strong> ${gweMin} feet</p>` +
    `<p><strong>Median GWE:</strong> ${gweMedian} feet</p>` +
    `<p><strong>Average GWE:</strong> ${gweAvg} feet</p>`
  );
}

// Function to calculate median
function calculateMedian(values) {
  values.sort((a, b) => a - b);
  var medianIndex = Math.floor(values.length / 2);
  if (values.length % 2 === 0) {
    return (values[medianIndex - 1] + values[medianIndex]) / 2;
  } else {
    return values[medianIndex];
  }
}

// Function to calculate average
function calculateAverage(values) {
  var sum = values.reduce((total, value) => total + value, 0);
  return sum / values.length;
}

// Sets the dates variable to be accessed by the function below
var filteredResults = [];

// Event listener for changes in start date and end date dropdown menus
function optionChanged(){
  var selectedStation = document.getElementById('selDataset').value;
  var startDate = new Date(document.getElementById('selStartDate').value);
  var endDate = new Date(document.getElementById('selEndDate').value);

  generateLineChart(filteredResults, startDate, endDate);
  generateHistogram(filteredResults, selectedStation);
  generateSiteData(selectedStation);
}
  
// Function to run on page load
function init() {
    d3.json("https://data.cnra.ca.gov/api/3/action/datastore_search?resource_id=af157380-fb42-4abf-b72a-6f9f98868077&limit=47000").then((data) => {
      var stations = data.result.records;
      
      // Selects dropdowns by ID
      var dropdown = d3.select('#selDataset');
      var startDateDropdown = d3.select('#selStartDate');
      var endDateDropdown = d3.select('#selEndDate');
  
      // Populates the options for site codes
      stations.forEach((station) => {
        dropdown.append('option').text(station.site_code).property('value', station.site_code);
      });
   
      // Defines a function to make an API call filtered by the selected site code
      function updateUrl(selectedStation){
        var stationFilteredUrl = `https://data.cnra.ca.gov/api/3/action/datastore_search?resource_id=bfa9f262-24a1-45bd-8dc8-138bc8107266&q=${selectedStation}`;
    
        // Makes the API call with the filtered URL
        d3.json(stationFilteredUrl).then((filteredData) => {
            filteredResults = filteredData.result.records;
    
            // Sorts the dates in ascending order
            filteredResults.sort((a, b) => new Date(a.msmt_date) - new Date(b.msmt_date));
    
            // Populates the date dropdown menus
            startDateDropdown.html(""); // Clears the previous options
            endDateDropdown.html(""); // Clears the previous options
            filteredResults.forEach((date) => {
                startDateDropdown.append('option').text(date.msmt_date).property('value', date.msmt_date);
                endDateDropdown.append('option').text(date.msmt_date).property('value', date.msmt_date);
            });
    
            // Retrieves the selected start and end dates for the plot
            var startDate = new Date(startDateDropdown.node().value);
            var endDate = new Date(endDateDropdown.node().value);
    
            // Generates a scatter plot for the data gathered within the selected date
            generateLineChart(filteredResults, startDate, endDate);
    
            // Generates a histogram for the selected site code
            generateHistogram(filteredResults);
    
            // Populates the site data panel
            generateSiteData(selectedStation);
    
            // Populates the stats data panel
            generateStatsData(filteredResults, selectedStation);
        });
    }
  
    // Event listener for changes in station site dropdown
    dropdown.on('change', function(){
      var stationDropdown = this.value;
      updateUrl(stationDropdown);
    });
  
    // Event listener for changes in start date
    startDateDropdown.on('change', function() {
        // Enable all end date options
        endDateDropdown.selectAll('option').property('disabled', false);

        // Disable end date options that are earlier than the selected start date
        var startDate = new Date(this.value);
        endDateDropdown.selectAll("option")
        .filter(function(d) { return new Date(d3.select(this).property("value")) < startDate; })
        .property("disabled", true);
    });

    // Event listener for changes in end date
    endDateDropdown.on('change', function() {
        // Enable all start date options
        startDateDropdown.selectAll('option').property('disabled', false);

        // Disable start date options that are later than the selected end date
        var endDate = new Date(this.value);
        startDateDropdown.selectAll("option")
        .filter(function(d) { return new Date(d3.select(this).property("value")) > endDate; })
        .property("disabled", true);
    });
  
    // Get the first sample from the list
    var firstSample = stations[0].site_code;
    updateUrl(firstSample);
    });
  }

  // Initialize the dashboard
  init();