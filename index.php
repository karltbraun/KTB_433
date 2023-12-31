<?php
// Define the file path and time interval
$dataFilePath = './Data/data.json';
//$refreshInterval = 2 * 60 * 1000; // 2 minutes in milliseconds
$refreshInterval = 15 * 1000; // 15 seconds

// Function to read and parse JSON data from the file
function readJsonData($filePath) {
    $jsonString = file_get_contents($filePath);
    return json_decode($jsonString, true);
}

// Function to format JSON data for display
function formatJsonData($jsonData) {
    $output = '';

    foreach ($jsonData as $entry) {
        if ($entry['sensor_name'] === 'unknown') {
            $output .= '<p>' . $entry['info'] . '</p>';
        } else {
            $output .= '<p>Sensor: ' . $entry['sensor_name'] . ', Temperature: ' . $entry['temperature'] . ', Humidity: ' . $entry['humidity'] . '</p>';
        }
    }

    return $output;
}

// Fetch JSON data from the file and display it
$jsonData = readJsonData($dataFilePath);
$jsonOutput = formatJsonData($jsonData);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSON Data Display</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
        }

        h1 {
            text-align: center;
        }

        p {
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <h1>JSON Data Display</h1>
    <div id="json-display">
        <?php echo $jsonOutput; ?>
    </div>

    <script>
        // Function to fetch JSON data from the PHP backend and update the page
        function fetchJsonData() {
            fetch('index.php')
                .then(response => response.text())
                .then(data => {
                    document.getElementById('json-display').innerHTML = data;
                })
                .catch(error => console.error('Error fetching JSON data:', error));
        }

        // Function to fetch JSON data on page load and refresh every few minutes
        function init() {
            fetchJsonData();
            setInterval(fetchJsonData, <?php echo $refreshInterval; ?>); // Refresh data every specified time interval
        }

        // Call the init function on page load
        window.onload = init;
    </script>
</body>
</html>
