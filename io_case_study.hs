--  http://book.realworldhaskell.org/read/io-case-study-a-library-for-searching-the-filesystem.html
--

import RecursiveContents

simpleFind :: (FilePath -> Bool) -> FilePath -> IO [FilePath]
simpleFind p path = do 
    names <- getRecursiveContents path
    return (filter p names)
