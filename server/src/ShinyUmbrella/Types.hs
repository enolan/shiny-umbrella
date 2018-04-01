module ShinyUmbrella.Types where

import ClassyPrelude

import Control.Lens
import Data.Aeson
import Data.UUID

data Msg a = Msg {_msgId :: UUID, _msgContent :: a}
  deriving (Generic, Show)
makeLenses ''Msg


data ClientMsg =
    Utterance (Vector (Vector Text))
  | Hypothesis
  | RecognitionStart
  deriving (Generic, Show)
makePrisms ''ClientMsg

data CorrectionData = CorrectionData {_correctID :: UUID, _correction :: Vector Text}
  deriving (Generic, Show)
makeLenses ''CorrectionData

data ServerMsg =
    Correction CorrectionData
  | MicOn
  | MicOff
  | RelinquishControl
  | ClaimControl
  deriving (Generic, Show)
makePrisms ''ServerMsg

jsonOptions :: Options
jsonOptions = defaultOptions {fieldLabelModifier = drop 1}

-- You can probably do this with TH but whatever.
instance ToJSON a => ToJSON (Msg a) where
  toJSON = genericToJSON jsonOptions
  toEncoding = genericToEncoding jsonOptions

instance ToJSON ClientMsg where
  toJSON = genericToJSON jsonOptions
  toEncoding = genericToEncoding jsonOptions

instance ToJSON CorrectionData where
  toJSON = genericToJSON jsonOptions
  toEncoding = genericToEncoding jsonOptions

instance ToJSON ServerMsg where
  toJSON = genericToJSON jsonOptions
  toEncoding = genericToEncoding jsonOptions

instance FromJSON a => FromJSON (Msg a) where
  parseJSON = genericParseJSON jsonOptions

instance FromJSON ClientMsg where
  parseJSON = genericParseJSON jsonOptions

instance FromJSON CorrectionData where
  parseJSON = genericParseJSON jsonOptions

instance FromJSON ServerMsg where
  parseJSON = genericParseJSON jsonOptions
