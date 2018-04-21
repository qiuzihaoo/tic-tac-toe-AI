-- phpMyAdmin SQL Dump
-- version 4.7.9
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 21, 2018 at 02:19 AM
-- Server version: 10.1.31-MariaDB
-- PHP Version: 7.2.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tictactoe`
--

-- --------------------------------------------------------

--
-- Table structure for table `longterm`
--

CREATE TABLE `longterm` (
  `id` int(11) NOT NULL,
  `board_before` varchar(10) NOT NULL,
  `move` int(11) NOT NULL,
  `board_after` varchar(10) NOT NULL,
  `score` int(11) NOT NULL,
  `role` char(1) NOT NULL,
  `explored` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `shortterm`
--

CREATE TABLE `shortterm` (
  `id` int(11) NOT NULL,
  `board_before` varchar(10) NOT NULL,
  `move` int(11) NOT NULL,
  `board_after` varchar(10) NOT NULL,
  `role` char(1) NOT NULL,
  `new` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `longterm`
--
ALTER TABLE `longterm`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `board_move` (`board_before`,`move`) USING BTREE;

--
-- Indexes for table `shortterm`
--
ALTER TABLE `shortterm`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `board_move` (`board_before`,`move`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `longterm`
--
ALTER TABLE `longterm`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `shortterm`
--
ALTER TABLE `shortterm`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
