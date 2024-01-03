<?php
// Sertakan file koneksi atau buat koneksi di sini
include("koneksi.php");

// Query untuk mendapatkan data terakhir
$queryLatest = "SELECT * FROM detect ORDER BY timestamp_added DESC LIMIT 1";
$resultLatest = $koneksi->query($queryLatest);

// Query untuk mendapatkan seluruh data
$queryAll = "SELECT * FROM detect";
$resultAll = $koneksi->query($queryAll);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <title>WOIOI</title>
</head>
<body>
    <header class="body-header">
        <h1>BIRD DETECTION DATA</h1>
    </header>
    <main class="dashboard-content">
        <!-- Container Data Terakhir dengan Flexbox -->
        <div class="flex-container">
            <div class="latest-data-container">
                <h2 class="latest-data-heading">Data Terakhir</h2>
                <div class="latest-data">
                    <?php
                        if ($resultLatest->num_rows > 0) {
                            $latestData = $resultLatest->fetch_assoc();
                            echo "<p>data_column: {$latestData['data_column']}</p>";

                            // Periksa apakah kunci "data_added" ada dalam array sebelum mengaksesnya
                            if (isset($latestData['data_added'])) {
                                echo "<p>data_added: {$latestData['data_added']}</p>";
                            } else {
                                echo "<p>data_added:</p>"; // Atau isi dengan nilai default sesuai kebutuhan
                            }

                            echo "<p>time_added: {$latestData['time_added']}</p>";
                            echo "<p>timestamp_added: {$latestData['timestamp_added']}</p>";
                        } else {
                            echo "<p class='no-data'>Tidak ada data.</p>";
                        }
                    ?>
                </div>
            </div>

            <!-- Tabel Data -->
            <h2 class="table-heading">Data Klien</h2>
            <table class="data-table">
                <thead>
                    <tr>
                        <th class="table-header">ID</th>
                        <th class="table-header">data_column</th>
                        <th class="table-header">data_added</th>
                        <th class="table-header">time_added</th>
                        <th class="table-header">timestamp_added</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                        // ...

                        if ($resultAll->num_rows > 0) {
                            while ($row = $resultAll->fetch_assoc()) {
                                echo "<tr>
                                        <td class='table-cell'>{$row['id']}</td>
                                        <td class='table-cell'>{$row['data_column']}</td>";

                                // Periksa apakah kunci "data_added" ada dalam array sebelum mengaksesnya
                                if (isset($row['data_added'])) {
                                    echo "<td class='table-cell'>{$row['data_added']}</td>";
                                } else {
                                    echo "<td class='table-cell'></td>"; // Atau isi dengan nilai default sesuai kebutuhan
                                }

                                echo "<td class='table-cell'>{$row['time_added']}</td>
                                    <td class='table-cell'>{$row['timestamp_added']}</td>
                                    </tr>";
                            }
                        } else {
                            echo "<tr><td class='no-data' colspan='5'>Tidak ada data Burung.</td></tr>";
                        }
                        // ...
                    ?>
                </tbody>
            </table>
        </div>
    </main>
</body>
</html>
