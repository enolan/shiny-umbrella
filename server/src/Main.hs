-- The server i.e. the side that controls the computer.
module Main where

import ClassyPrelude

import Data.Aeson
import Network.Connection
import Network.Socket
import System.Exit

import ShinyUmbrella.Types

main :: IO ()
main =
  bracket
    (socket AF_INET Stream defaultProtocol)
    close
    $ \lsock -> do
      let saddr = SockAddrInet 43238 $ tupleToHostAddress (192,168,56,1)
      bind lsock saddr
      listen lsock 1
      connCtx <- initConnectionContext
      forever $ bracket
        (accept lsock)
        (close . fst)
        $ \(sock, incomingSaddr) -> do
          putStrLn $ "Accepted connection from " <> pack (show incomingSaddr)
          conn <- connectFromSocket connCtx sock $
            ConnectionParams "incoming" 0 Nothing Nothing
          catch
            (serverLoop conn)
            (\(ex :: SomeException) -> putStrLn $
                "exception in server loop: " <> pack (show ex))

serverLoop :: Connection -> IO ()
serverLoop conn = forever $ do
  msg <- connectionGetLine 8192 conn
  case eitherDecodeStrict msg of
    Left err -> putStrLn (pack err) >> exitFailure
    Right msg' -> handleMsg msg'
  where
  handleMsg :: Msg ClientMsg -> IO ()
  handleMsg msg = print msg
