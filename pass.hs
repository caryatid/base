import System.IO
import Control.Monad
import Data.Char
import Data.Maybe

getPassword :: IO (Maybe String)
getPassword = do 
                 s <- getLine
                 if isValid s then return $ Just s
                              else return Nothing

isValid :: String -> Bool
isValid s = length s >= 8 && any isAlpha s && any isNumber s &&
            any isPunctuation s


askPassword :: IO ()
askPassword = do putStrLn "monkey junky: "
                 pw <- getPassword
                 if isJust pw
                     then do putStrLn "Storing..."
                     else askPassword
                        
                                 
