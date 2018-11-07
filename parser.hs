{-# LANGUAGE OverloadedStrings #-}
{-# LANGUAGE TemplateHaskell   #-}

import           Data.Aeson
import           Data.ByteString.Lazy as B
import           Data.Text            as T
import           Data.Text.IO         as TIO
import           Text.Pandoc
import           Text.Pandoc.Walk

removeMeta :: Pandoc -> Pandoc
removeMeta (Pandoc _ a) = Pandoc nullMeta a

removeLinks :: Pandoc -> Pandoc
removeLinks = walk remove
  where remove :: Inline -> Inline
        remove (Link _ _ _) = Str ""
        remove (Span _ _)   = Str ""
        remove x            = x

clean :: Pandoc -> Pandoc
clean a = removeLinks $ removeMeta a

extractMath :: Pandoc -> [Text]
extractMath = query eqns
  where eqns (Math _ u) = [T.pack u]
        eqns _          = []

extractStrings :: Pandoc -> [Text]
extractStrings = query strings
  where strings (Str u) = [T.pack u]
        strings _       = []

val :: Pandoc -> Value
val a = object [
  "Text" .= extractStrings (clean a),
  "Math" .= extractMath (clean a)]

main :: IO ()
main = do
  raw <- TIO.getContents
  result <- runIO $ do
    readLaTeX def raw
  doc <- handleError result

  let contents = encode $ val doc

  B.putStr contents

