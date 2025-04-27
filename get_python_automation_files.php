<?php
// Set appropriate headers for JSON response
header('Content-Type: application/json');
header('Cache-Control: no-cache, no-store, must-revalidate');
header('Pragma: no-cache');
header('Expires: 0');

// Configure error reporting
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Directory to scan
$directory = './';

// Get all HTML files in the directory
$files = glob($directory . 'python_automation_*.html');

// Filter files that start with 'python_automation_'
$pythonAutomationFiles = array_filter($files, function($file) {
    return strpos(basename($file), 'python_automation_') === 0;
});

// Sort the files naturally to ensure correct chapter/slide order
natcasesort($pythonAutomationFiles);

// Convert full paths to relative paths (just the filenames)
$relativeFiles = array_map('basename', $pythonAutomationFiles);

// Output the file list as JSON
echo json_encode(array_values($relativeFiles));
?> 