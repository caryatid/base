-- takes an argument and [0..] and switches the wacom to that monitor
--
--
-- use doctest for this to help plan it out
--

{- |
 - module wacom
 - only switch screen for now
 -}

module WacomControl where
import System.Environment
import System.Process


main = getArgs >>= parse 

parse ["0"] = rawSystem "xsetwacom" ["set", "Wacom Bamboo 16FG 4x5 Pen stylus", "MapToOutput", 
    "HDMI1"]
parse ["1"] = rawSystem "xsetwacom" ["set", "Wacom Bamboo 16FG 4x5 Pen stylus", "MapToOutput", 
    "VGA1"]




