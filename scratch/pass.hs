import System.IO
import Control.Monad
import Control.Monad.Trans.Class
import Data.Char
import Data.Maybe
import Control.Monad.State
import System.Random

getPassword :: IO (Maybe String)
getPassword = do 
                 s <- getLine
                 if isValid s then return $ Just s
                              else return Nothing

isValid :: String -> Bool
isValid s = length s >= 8 && any isAlpha s && any isNumber s &&
            any isPunctuation s


--  askPassword :: IO ()
--  askPassword = do putStrLn "monkey junky: "
                 --  pw <- getPassword
                 --  if isJust pw
                     --  then do putStrLn "Storing..."
                     --  else askPassword


newtype MaybeT m a = MaybeT { runMaybeT :: m (Maybe a) }

instance Monad m => Monad (MaybeT m) where
        return = MaybeT . return . return
        (>>=) m f = MaybeT $ do v <- runMaybeT m
                                case v of
                                    Nothing -> return Nothing
                                    Just x -> runMaybeT $ f x

instance Monad m => MonadPlus (MaybeT m) where
        mzero = MaybeT $ return Nothing
        mplus x y = MaybeT $ do mval <- runMaybeT x
                                case mval of
                                    Nothing -> runMaybeT y
                                    Just _  -> return mval

instance MonadTrans MaybeT where
        lift = MaybeT . (liftM Just)

getValidPassword :: MaybeT IO String
getValidPassword = do s <- lift getLine
                      guard (isValid s)
                      return s

askPassword :: MaybeT IO ()
askPassword = do lift $ putStrLn "New password: "
                 val <- msum $ repeat getValidPassword
                 lift $ putStrLn "Storing pw:"
   
--  tester :: MonadState StdGen Int
--  tester = do 
            --  s <- get
            --  y <- state random
            --  return y
main = do
        runMaybeT askPassword

