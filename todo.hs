-- todo stuff

{- 
 -- questions
 ------------
 - what are the todo indexen
 - what am I doing [time]
 -}
{- 
 -- requirements 
 ---------------
 - todo data 
 -- name
 -- id
 -- location
 -- contents
 - 
 - goal data
 -- active timestamps
 - 
 - timeboxen data
 -- [timebox]
 -- main
 -- daily
 -- anti-main
 -- secondary
 -- anti-secondary
 - timebox
 -- [section_type:list]
 - start box
 -- set of questions like:
 --- current boxen are a,b,c,d,e is this good?
 --- how did your schedule work yesterday?
 ---- talk about [x for x in timeboxen]
 - end box
 -- todo of fun shit from a fun shit list
 -- this is where I wonder if I need friends.
 - priorites
 -- store a uuid:goal:level type file list
 -- must have technique for cleaning up when UUID's go away
 -}


--  +-----------------------------------------------------------------+
--  | +|...................................// all about them //---|{{{|
--  |  |TODO|  all about them                                         |
--  |                                                                 |
--  | +|.............// dc590064-3fd4-4b9e-ab46-e356d7923e2d //---|}}}|
--  +-----------------------------------------------------------------+ 

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
    mapM putStrLn  text
