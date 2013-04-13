
{-# LANGUAGE DeriveDataTypeable #-}

import XMonad
import XMonad.Util.ExtensibleState as XS
import Control.Monad
import Text.Regex.Posix
import System.IO
import Data.List
import Data.Colour as DC
import Data.Colour.Names
import Data.Colour.SRGB
import Control.Applicative
-- terminal colors
data TColor = TRed | TGreen | TBlue
            deriving (Enum, Bounded, Eq)

-- state holding current terminal color
data TColorState = TColorState TColor
                 deriving Typeable

instance ExtensionClass TColorState
        where
            initialValue = TColorState TRed

data ColorSet a b = ColorSet [(a,b)]
              deriving (Show)
-- colors for urxvt
rxvtArgs :: [String]
rxvtArgs = zipWith (++) pre post
    where pre = repeat "--"
          post = [ "cursorColor"
                 , "foreground"
                 , "background"] ++ 
                 (take 16 $ ["color" ++ (show x) | x <- [0..]])
rxvtColors :: [String] -> [String]            
rxvtColors = zipWith (++) (repeat "#")

--  lessColor :: (Fractional a, Ord a, ColourOps f) => a -> f a -> [f a]
lessColor n x  
        | n < 0 = []
        | otherwise = (sRGB24show $ darken n x) : lessColor (n - 0.03) x

genColorSet = let x = zip rxvtArgs $ lessColor 1 red
                  in map (\(a,b) -> a ++ " " ++ b) x

test :: X ()
test = do
        spawn $  intercalate " " $ ["urxvt"] ++ genColorSet

                
darker16 c = map (flip darken c) $ map (\x -> x / 16) [1..16] 

-- convert a color to a shell-escaped X11 color spec
tColor :: TColor -> (String, String)
tColor TBlue   = ("\\#A8CCEA", "\\#012645")
tColor TGreen = ("\\#5BECB5", "\\#00482D")
tColor TRed  = ("\\#FFDEB1", "\\#95593E")

-- get the current terminal color and save the next one to use
tRotate :: X (String, String)
tRotate = do
        (TColorState c) <- XS.get
        XS.put . TColorState $ if c == maxBound then minBound else succ c
        return $ tColor c

-- spawn a terminal with a rotating background color
colorTerminal :: X ()
colorTerminal = do
        (l,d) <- tRotate -- light, dark
        term <- asks $ terminal . config
        spawn $ term ++ " -fg " ++ d ++ " -bg " ++ l
