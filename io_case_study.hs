--  http://book.realworldhaskell.org/read/io-case-study-a-library-for-searching-the-filesystem.html
--

import RecursiveContents
import System.Directory (Permissions(..), getModificationTime, getPermissions)
import Control.Monad (filterM)
import System.Time (ClockTime(..))
import System.FilePath (takeExtension)
import Control.Exception (bracket, handle)
import System.IO (IOMode(..), hClose, hFileSize, openFile)
import Data.Time

type Predicate = FilePath
    -> Permissions
    -> Maybe Integer
    -> UTCTime
    -> Bool

getFileSize :: FilePath -> IO (Maybe Integer)
getFileSize a = undefined

betterFind :: Predicate -> FilePath -> IO [FilePath]

betterFind p path = getRecursiveContents path >>= filterM check
    where check name = do
            perms <- getPermissions name
            size <- getFileSize name
            modified <- getModificationTime name
            return (p name perms size modified)

simpleFileSize path = do
    h <- openFile path ReadMode
    size <- hFileSize h
    hClose h
    return size


saferFileSize path = handle (\_ -> return Nothing) $ do
    h <- openFile path ReadMode
    size <- hFileSize h
    hClose h
    return (Just size)

simpleFind :: (FilePath -> Bool) -> FilePath -> IO [FilePath]
simpleFind p path = do 
    names <- getRecursiveContents path
    return (filter p names)


    
