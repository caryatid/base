-- | import Network
-- | import System.IO
-- | import System.Process
-- | import Data.List
-- | import Control.Monad.State
-- | {- import Control.Concurrent -}
-- | 
-- | 
-- | main = withSocketsDo $ do
    -- | sock <- listenOn (PortNumber 12345)
    -- | loop sock
-- | 
-- | loop sock = do
    -- | (h,_,_) <- accept sock
    -- | d <- hGetContents h
    -- | putStrLn d

-- | main = do 
    -- | x <- readProcess "/usr/bin/git" ["status"] ""
    -- | y <- return $ takeWhile  (not . isInfixOf "Untrack") (lines x)
    -- | putStrLn $ unlines y

{- 
+-----------------------// State Monad // ---
 | TODO | State Monad from http://www.haskell.org/haskellwiki/State_Monad

return x s = (x,s) 
(>>=) :: State s a -> (a -> State s b) -> State s b
(act1 >>= fact2) s = runState act2 is 
    where (iv,is) = runState act1 s
          act2 = fact2 iv
get >>= (\(_,score) -> return score)

runState act2 is
    where (iv, is) = runState get s
              act2 = (\(_,score) -> return score) iv
              
runState act2 (Int,(Bool,Int))
    where (GameValue, GameState = runState get s
              act2 = (\(_,score) -> return score) GameValue
              
runState 


 -}


import Control.Monad.State

import System.Random

clumsyRollDice :: (Int, Int)
clumsyRollDice = (n, m) 
    where 
        (n, g) = randomR (1,6) (mkStdGen 0)
        (m, _) = randomR (1,6) g
        
-- | main = putStrLn "hello"

type GeneratorState = State StdGen

rollDie :: GeneratorState Int
rollDie = do
    gen <- get
    let (val, newGen) = randomR (1,6) gen
    put newGen
    return val

rollDice :: GeneratorState (Int, Int, Int)
rollDice = liftM3 (,,) rollDie rollDie rollDie
    
-- | +-----

-- | +-----------------------// lifting break // ---
-- | | TODO | lifting : http://www.haskell.org/haskellwiki/Lifting

data Pair a = Pair a a deriving (Show)

instance Functor Pair where
    fmap f (Pair x y) = Pair (f x) (f y)
    
lift :: (a -> b) -> (Pair a -> Pair b)
lift = fmap

lift2 :: (a -> b -> c) -> (Pair a -> Pair b -> Pair c)
lift2 f (Pair x y) (Pair x1 y1) = Pair (f x x1) (f y y1)


-- | +-----


-- function that increments state

foo :: Int -> (String, Int)
foo x = ("dumb", x+1)

foo2 :: String -> State Int [String]
foo2 z = state (\x -> (["lame","nice", z], x+10))

-- data Either' e a = Le e 
--                    | Ri a


-- instance Functor (Either' e) where
--        fmap _ (Le e) = Le e
--        fmap f (Ri a) = Ri $ f a


-- instance Functor ((->) e) where
--         fmap g x = g . x

-- instance Functor ((,) e) where
--         fmap g (a, b) = (a, g b)

-- data Pair a = Pair a a

-- instance Functor Pair where
--         fmap f (Pair a b) = Pair (f a) (f b)

data ITree a = Leaf (Int -> a)
        | Node [ITree a]
        deriving(Show)

instance Functor ITree where
        fmap f (Leaf g) = Leaf $ f . g
        fmap f (Node xs) = Node $ fmap (fmap f) xs


main = do
    let x = 0
        -- | (a, b) = runState (get >> state foo) 10 
        -- | (a, b) = runState (get >> return "value" >> state foo) 10 
        (a, b) = runState now 10
                    where now = do 
                            s <- get
                            z <- return "yaya"
                            val <- foo2 z
                            state foo
                            return $ show val  
    putStrLn $ "hello" ++ (show b) ++ a
