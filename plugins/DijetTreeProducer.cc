#include <iostream>
#include <sstream>
#include <istream>
#include <fstream>
#include <iomanip>
#include <string>
#include <cmath>
#include <functional>
#include <vector>
#include <cassert>
#include "TFile.h"
#include "TH1D.h"
#include "TMath.h"
#include "TLorentzVector.h"

#include "CMSDIJET/DijetRootTreeMaker/plugins/DijetTreeProducer.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/JetCollection.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
//#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
//#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

using namespace std;
using namespace reco;
using namespace pat;
using namespace edm;

DijetTreeProducer::DijetTreeProducer( const ParameterSet & cfg )
{ 
  srcToken_      = ( consumes<edm::View<reco::Candidate> >(cfg.getParameter<InputTag>( "src" ) ) );
  printP4_       = ( cfg.getUntrackedParameter<bool>( "printP4", false ) );
  printPtEtaPhi_ = ( cfg.getUntrackedParameter<bool>( "printPtEtaPhi", false ) );
  printVertex_   = ( cfg.getUntrackedParameter<bool>( "printVertex", false ) );
  printStatus_   = ( cfg.getUntrackedParameter<bool>( "printStatus", false ) );
  printIndex_    =  ( cfg.getUntrackedParameter<bool>( "printIndex", false ) );
  status_        = ( cfg.getUntrackedParameter<vint>( "status", vint() ) ) ;
}

bool DijetTreeProducer::accept( const reco::Candidate & c ) const {
  if ( status_.size() == 0 ) return true;
  return find( status_.begin(), status_.end(), c.status() ) != status_.end();
}

bool DijetTreeProducer::hasValidDaughters( const reco::Candidate & c ) const {
  size_t ndau = c.numberOfDaughters();
  for( size_t i = 0; i < ndau; ++ i )
    if ( accept( * c.daughter( i ) ) )
      return true;
  return false;
}
/*
std::string DijetTreeProducer::getParticleName(int id) const {
  const ParticleData * pd = pdt_->particle( id );
  if (!pd) {
    std::ostringstream ss;
    ss << "P" << id;
    return ss.str();
  } else
    return pd->name();
}
*/
void DijetTreeProducer::printInfo( const Candidate & c ) const {
  if ( printP4_ ) cout << " (" << c.px() << ", " << c.py() << ", " << c.pz() << "; " << c.energy() << ")";
  if ( printPtEtaPhi_ ) cout << " [" << c.pt() << ": " << c.eta() << ", " << c.phi() << "]";
  if ( printVertex_ ) cout << " {" << c.vx() << ", " << c.vy() << ", " << c.vz() << "}";
  if ( printStatus_ ) cout << "{status: " << c.status() << "}";
  if ( printIndex_ ) {
    int idx = -1;
    vector<const Candidate *>::const_iterator found = find( cands_.begin(), cands_.end(), & c );
    if ( found != cands_.end() ) {
      idx = found - cands_.begin();
      cout << " <idx: " << idx << ">";
    }
  }
}

void DijetTreeProducer::printDecay( const Candidate & c, const string & pre ) const {
//  cout << getParticleName( c.pdgId() );
  cout<<c.pdgId();
  printInfo( c );
  cout << endl;

  size_t ndau = c.numberOfDaughters(), validDau = 0;
  for( size_t i = 0; i < ndau; ++ i )
    if ( accept( * c.daughter( i ) ) )
      ++ validDau;
  if ( validDau == 0 ) return;

  bool lastLevel = true;
  for( size_t i = 0; i < ndau; ++ i ) {
    if ( hasValidDaughters( * c.daughter( i ) ) ) {
      lastLevel = false;
      break;
    }
  }

  if ( lastLevel ) {
    cout << pre << "+-> ";
    size_t vd = 0;
    for( size_t i = 0; i < ndau; ++ i ) {
      const Candidate * d = c.daughter( i );
      if ( accept( * d ) ) {

    cout << d->pdgId();  // getParticleName( d->pdgId() );
    printInfo( * d );
    if ( vd != validDau - 1 )
      cout << " ";
    vd ++;
      }
    }
    cout << endl;
    return;
  }

  for( size_t i = 0; i < ndau; ++i ) {
    const Candidate * d = c.daughter( i );
    assert( d != 0 );
    if ( accept( * d ) ) {
      cout << pre << "+-> ";
      string prepre( pre );
      if ( i == ndau - 1 ) prepre += "    ";
      else prepre += "|   ";
      printDecay( * d, prepre );
    }
  }
}

//DijetTreeProducer::DijetTreeProducer(edm::ParameterSet const& cfg)
//DijetTreeProducer::DijetTreeProducer( const ParameterSet& cfg)
//{
//}

  
  
//////////////////////////////////////////////////////////////////////////////////////////
void DijetTreeProducer::beginJob() 
{


}
//////////////////////////////////////////////////////////////////////////////////////////
void DijetTreeProducer::endJob() 
{  


}
//////////////////////////////////////////////////////////////////////////////////////////
void DijetTreeProducer::analyze(edm::Event const& iEvent, edm::EventSetup const& iSetup)
// edm::ParameterSet const& cfg
{
  initialize();
  Handle<View<Candidate> > particles;
  iEvent.getByToken( srcToken_, particles );
  cands_.clear();
  for( View<Candidate>::const_iterator p = particles->begin();
       p != particles->end(); ++ p ) {
    cands_.push_back( & * p );
  }
  for( View<Candidate>::const_iterator p = particles->begin();
       p != particles->end(); ++ p ) {
    if ( accept( * p ) ) {
      if ( p->mother() == 0 ) {
    cout << "-- decay tree: --" << endl;
    printDecay( * p, "" );
      }
    }
  }    
  
  
}//end analyze for each event

//////////////////////////////////////////////////////////////////////////////////////////
void DijetTreeProducer::initialize()
{
  
}
//////////////////////////////////////////////////////////////////////////////////////////
DijetTreeProducer::~DijetTreeProducer() 
{
}

DEFINE_FWK_MODULE(DijetTreeProducer);
