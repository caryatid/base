import System.IO
import Control.Monad
import Data.Complex
import System.Random

--  +|.........................// Debugging pure functions //---|{{{
 --  |TODO|  Debugging pure functions
--  f,g :: Float -> Float
--  f = log
--  g = logBase 10


--  f',g' :: Float -> (Float,String)

--  f' x = (f x, "f prime " ++ show x)
--  g' x = (g x, "g prime " ++ show x)


--  bind :: (Float -> (Float,String)) -> (Float, String) -> (Float,String)
--  bind f' (gx, gs) = let (fx,fs) = f' gx 
                       --  in (fx, gs ++ fs)

--  unit :: a -> (a, String)
--  unit x = (x , "")

--  lift f  = unit . f


--  mainW = do let (n,s) = bind (lift g) (lift f 10)
               --  (x,y) = lift (g . f) 10
          --  putStrLn $ show n
          --  putStrLn $ show x
--  +|.............// 6ec5a842-ac00-4382-a262-57834edcefb9 //---|}}}

--  +|............................// Multivalued Functions //---|{{{
 --  |TODO|  Multivalued Functions

--  sqrt',cbrt' :: Complex Float -> [Complex Float]
--  sixthroot x = sqrt (cbrt x)

--  bindL :: (Complex Double -> [Complex Double]) -> ([Complex Double] -> [Complex Double])
--  bindL f x = concat (map f x)
--  unitL :: Complex Double -> [Complex Double]
--  unitL x = [x]
--  liftL f = unitL . f
--  (<.>) f g = bindL f . g

--  xs = bindL (liftL sqrt) (liftL (^3) (10 :: Complex Double))

--  +|.............// 026d97a1-75b2-482b-8fb9-9cfa89fec52c //---|}}}

--  +|.................................// Random [ state ] //---|{{{
 --  |TODO|  Random [ state ]

bindR :: (a -> StdGen -> (b, StdGen)) -> (StdGen -> (a, StdGen)) -> (StdGen -> (b, StdGen))
bindR f x seed = let (x', seed') = x seed
                     in f x' seed'

unitR :: a -> (StdGen -> (a, StdGen))
unitR x = (\g -> (x,g))

(xx) f g = bindR f . g

--  +|.............// 71f95a5f-679c-497c-95a3-70c892f344c1 //---|}}}
