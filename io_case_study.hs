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

handler :: IOError -> IO (Maybe a)
handler x = return Nothing

type Predicate = FilePath
    -> Permissions
    -> Maybe Integer
    -> UTCTime
    -> Bool

getFileSize :: FilePath -> IO (Maybe Integer)
getFileSize path = handle handler $
    bracket (openFile path ReadMode) hClose $ \h -> do
        size <- hFileSize h
        return (Just size)

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


saferFileSize path = handle handler $ do
    h <- openFile path ReadMode
    size <- hFileSize h
    hClose h
    return (Just size)

simpleFind :: (FilePath -> Bool) -> FilePath -> IO [FilePath]
simpleFind p path = do 
    names <- getRecursiveContents path
    return (filter p names)


type InfoP a = FilePath
    -> Permissions
    -> Maybe Integer
    -> UTCTime
    -> a

{- pathP :: InfoP FilePath -}


sizeP :: InfoP Integer
sizeP _ _ (Just size) _ = size
sizeP _ _ Nothing _ = -1


equalP :: (Eq a) => InfoP a -> a -> InfoP Bool
equalP f k w x y z = f w x y z == k
