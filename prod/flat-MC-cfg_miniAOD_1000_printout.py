import FWCore.ParameterSet.Config as cms 

process = cms.Process('jetToolbox')

process.load('PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')

## ----------------- Global Tag ------------------
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

#process.GlobalTag.globaltag = THISGLOBALTAG
process.GlobalTag.globaltag = '94X_mc2017_realistic_v13'


#--------------------- Report and output ---------------------------

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 5000


process.TFileService=cms.Service("TFileService",
                                 #fileName=cms.string('test_1000.root'),
                                 fileName=cms.string('/tmp/bStar_1000GeV.root'),
                                 closeFileFast = cms.untracked.bool(True)
                                 )

## --- suppress long output ---> wantSummary = cms.untracked.bool(False) 

process.options = cms.untracked.PSet(
        allowUnscheduled = cms.untracked.bool(True),
        wantSummary = cms.untracked.bool(False),
)

############## output  edm format ###############
process.out = cms.OutputModule('PoolOutputModule',                                                                                                                  
                               fileName = cms.untracked.string('jettoolbox.root'),                                                                              
                               outputCommands = cms.untracked.vstring([
                                                                      'keep *_slimmedJets_*_*',                                                                  
                                                                       ])                                                                                           
                               )


# ----------------------- Jet Tool Box  -----------------
# ----- giulia test: do not recluster ak4 and ca8 jets to save time --------

process.chs = cms.EDFilter('CandPtrSelector', src = cms.InputTag('packedPFCandidates'), cut = cms.string('fromPV'))

from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets


#-------------------------------------------------------
# Gen Particles Pruner
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.prunedGenParticlesDijet = cms.EDProducer('GenParticlePruner',
    src = cms.InputTag("prunedGenParticles"),
    select = cms.vstring(
    "drop  *  ", # by default
    "keep ( status = 3 || (status>=21 && status<=29) )", # keep hard process particles
    )
)


#------------- Recluster Gen Jets to access the constituents -------
#already in toolbox, just add keep statements

process.out.outputCommands.append("keep *_slimmedGenJets_*_*")

##-------------------- Define the source  ----------------------------


readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()
process.source = cms.Source ("PoolSource",

fileNames = cms.untracked.vstring(
#'file:/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/Generation/MinBias/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_miniAODv2_Tyler3000GeV_2RECO/181123_063352/0000/RSGravitonToQuarkQuark_kMpl01_M_3000_TuneCUETP8M1_13TeV_pythia8_RECO_218.root',
#'file:/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/Generation/MinBias/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_miniAODv2_Tyler3000GeV_2RECO/181123_063352/0000/RSGravitonToQuarkQuark_kMpl01_M_3000_TuneCUETP8M1_13TeV_pythia8_RECO_215.root',
#'file:/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/Generation/MinBias/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_miniAODv2_Tyler3000GeV_2RECO/181123_063352/0000/RSGravitonToQuarkQuark_kMpl01_M_3000_TuneCUETP8M1_13TeV_pythia8_RECO_216.root',
#'file:/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/Generation/MinBias/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_miniAODv2_Tyler3000GeV_2RECO/181123_063352/0000/RSGravitonToQuarkQuark_kMpl01_M_3000_TuneCUETP8M1_13TeV_pythia8_RECO_217.root'


#'file:/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/Generation/MinBias/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_miniAODv2_Tyler_1000GeV2RAW/181120_044853/0000/RSGravitonToQuarkQuark_kMpl01_M_2000_TuneCUETP8M1_13TeV_pythia8_GEN-SIM-RAW_913.root',
#'file:/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/Generation/MinBias/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_miniAODv2_Tyler_1000GeV2RAW/181120_044853/0000/RSGravitonToQuarkQuark_kMpl01_M_2000_TuneCUETP8M1_13TeV_pythia8_GEN-SIM-RAW_923.root',
#'file:/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/Generation/MinBias/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_miniAODv2_Tyler_1000GeV2RAW/181120_044853/0000/RSGravitonToQuarkQuark_kMpl01_M_2000_TuneCUETP8M1_13TeV_pythia8_GEN-SIM-RAW_933.root',
#'file:/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/Generation/MinBias/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_miniAODv2_Tyler_1000GeV2RAW/181120_044853/0000/RSGravitonToQuarkQuark_kMpl01_M_2000_TuneCUETP8M1_13TeV_pythia8_GEN-SIM-RAW_943.root',
#'file:/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/Generation/MinBias/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_miniAODv2_Tyler_1000GeV2RAW/181120_044853/0000/RSGravitonToQuarkQuark_kMpl01_M_2000_TuneCUETP8M1_13TeV_pythia8_GEN-SIM-RAW_953.root',
#'file:/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/Generation/MinBias/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_miniAODv2_Tyler_1000GeV2RAW/181120_044853/0000/RSGravitonToQuarkQuark_kMpl01_M_2000_TuneCUETP8M1_13TeV_pythia8_GEN-SIM-RAW_963.root',

'file:/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/Generation/MinBias/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_miniAODv2_Tyler/181105_213047/0001/RSGravitonToQuarkQuark_kMpl01_M_4000_TuneCUETP8M1_13TeV_pythia8_GEN-SIM_1982.root',
'file:/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/Generation/MinBias/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_miniAODv2_Tyler/181105_213047/0001/RSGravitonToQuarkQuark_kMpl01_M_4000_TuneCUETP8M1_13TeV_pythia8_GEN-SIM_1182.root',
'file:/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/Generation/MinBias/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_miniAODv2_Tyler/181105_213047/0001/RSGravitonToQuarkQuark_kMpl01_M_4000_TuneCUETP8M1_13TeV_pythia8_GEN-SIM_1282.root',
'file:/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/Generation/MinBias/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_miniAODv2_Tyler/181105_213047/0001/RSGravitonToQuarkQuark_kMpl01_M_4000_TuneCUETP8M1_13TeV_pythia8_GEN-SIM_1382.root',
'file:/eos/cms/store/group/phys_exotica/dijet/Dijet13TeV/TylerW/Generation/MinBias/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_miniAODv2_Tyler/181105_213047/0001/RSGravitonToQuarkQuark_kMpl01_M_4000_TuneCUETP8M1_13TeV_pythia8_GEN-SIM_1482.root',

)
)

#process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring('file:QstarToJJ_M_4000_TuneCUETP8M1_13TeV_pythia8__MINIAODSIM__Asympt50ns_MCRUN2_74_V9A-v1__70000__AA35D1E7-FEFE-E411-B1C5-0025905B858A.root')    
    #fileNames = cms.untracked.vstring('/store/mc/RunIISpring15DR74/QstarToJJ_M_1000_TuneCUETP8M1_13TeV_pythia8/AODSIM/Asympt50ns_MCRUN2_74_V9A-v1/50000/00F85752-BCFB-E411-A29A-000F5327349C.root')
    #fileNames = cms.untracked.vstring('root://xrootd.unl.edu//store/mc/RunIISpring15DR74/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/50000/0E4CEBFE-ECFB-E411-9F0C-842B2B29273C.root')
#    fileNames = cms.untracked.vstring(
#'/store/mc/RunIISummer17MiniAOD/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/92X_upgrade2017_realistic_v10-v2/00000/00569FE4-53AC-E711-B286-02163E014B86.root'
#)
#    fileNames = cms.untracked.vstring('/store/mc/RunIIFall17MiniAOD/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/MINIAODSIM/94X_mc2017_realistic_v11_ext1-v1/70000/041AA818-0820-E811-8B46-02163E01A0A4.root')

 #   )




##-------------------- User analyzer  --------------------------------

#Residue from deleted reco and AOD sequences
calo_collection=''
cluster_collection=''
pfcalo_collection=''
   

#process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.printTree = cms.EDAnalyzer("DijetTreeProducer",
                                   src = cms.InputTag("genParticles"),
                                   printP4 = cms.untracked.bool(False),
                                   printPtEtaPhi = cms.untracked.bool(False),
                                   printVertex = cms.untracked.bool(False),
                                   printStatus = cms.untracked.bool(False),
                                   printIndex = cms.untracked.bool(False),
                                   status = cms.untracked.vint32(21,22,23,24,25,26,27,28,29)
                                   )



# ------------------ path --------------------------

process.p = cms.Path(process.printTree)
