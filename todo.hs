-- todo stuff

{-|
--| how was your last day, generally?

--| [obj | obj <- ["primary/secondary", "alternate", "habit"]
--| Your obj goal is foo, would you like it to remain?
--| Current obj.goal todos:
--| how did your  obj.goal go?

--| your daily todos are:
--| any from yesterday need to take precedence?



-}


import System.FilePath
import RecursiveContents
import Data.List
import System.IO
import Control.Monad
type Uuid = String

data Todo = Todo { name :: String
        , id :: Uuid
        , location :: FilePath
        , contents :: [String]
        , priority :: Maybe Int -- if Nothing then unset
        , goal :: String
}

{-
 - instance of Read/Show
 - Read returns an mempty or mzero or whatever if not valid todo shit
 - header '+|.....// //...|' toggles 

a = "/home/dave/.timebox/goals/base"
getFlist :: FilePath -> IO [String]
getFlist  = getRecursiveContents 

procFile :: FilePath -> IO [String]
procFile fn = do
    txt <- withFile fn ReadMode hGetContents
    return $ lines txt

-- | Main 
--
main  = do 
    fname <- getRecursiveContents a
    fn_less <- return $ filter (not . isInfixOf ".git")  fname
    text <- concat $ mapM procFile  (take 4 fn_less)
    mapM putStrLn $ text
