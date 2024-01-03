<?php

$host = "localhost"; // Ganti dengan nama host database Anda
$user = "root"; // Ganti dengan nama pengguna database Anda
$password = ""; // Ganti dengan kata sandi database Anda
$database = "pysql"; // Ganti dengan nama database Anda

$koneksi = new mysqli("localhost", "root", "", "pysql");

if ($koneksi->connect_error) {
    die("Koneksi Gagal: " . $koneksi->connect_error);
}
?>
