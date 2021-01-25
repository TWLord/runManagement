// Fill from ASCII files into a bunch of TH1F

{

 
  TH2F *bx = new TH2F("bx", "Bx (T) vs z", 100, 0., 4000., 1000, 0, 1.);
  TH2F *by = new TH2F("by", "By (T) vs z", 100, 0., 4000., 1000, 0, .5);
  TH2F *bz = new TH2F("bz", "Bz (T) vz z", 100, 0., 4000., 1000, 0, 1.);

  TH2F *by_x = new TH2F("by_x", "By (T) vs x", 100, -200., 200., 1000, -20, .5);
 

  TNtuple *ntuple1 = new TNtuple("ntuple1","data from ascii file","x:y:z:Bx:By:Bz");
  //TNtuple *ntuple6 = new TNtuple("ntuple6","data from ascii file","Px:Py:Pz:PDGid:t");


  Float_t x, y, z, t, Px, Py, Pz, Bx, By, Bz, Ex, Ey, Ez;
  Int_t PDGid, EventID;
  string dummy;
  
  ifstream is;
  //  is.open("D1_field.txt");
  is.open("Q1_field2.txt");
  
  getline(is,dummy);
  getline(is,dummy);
  while (is.good())
    {
      is >> x >> y >> z >> t >> Bx >> By >> Bz >> Ex >> Ey >> Ez;
      ntuple1->Fill(x,y,z,Bx,By,Bz);
    }
  is.close();
  


  TCanvas *c1 = new TCanvas("c1", "G4BL simulation", 1400 , 600);
  //  c1->Divide(3,2);
  //c1->SetLogy();

  //  gStyle->SetPalette(1,0);
  gStyle->SetOptStat(0);

  //TCut cut1 = "sqrt(Px*Px+Py*Py)<0.15*abs(Pz)";
  TCut cut1 = ""; //"sqrt(Px*Px)<0.10*abs(Pz)";

  // Fill the canvas:

  //  ntuple1->Draw("Bx:z >> bz","PDGid==-13"&&cut1);
  //  bz->Draw("colz");
  //  c1.SaveAs("magnetic_field_Bx.png");

  //  ntuple1->Draw("By:z >> bz","PDGid==-13"&&cut1);
  //  bz->Draw("colz");
  //  c1.SaveAs("magnetic_field_By.png");




  ntuple1->Draw("Bx:z >> bx",cut1);
  ntuple1->Draw("By:z >> by",cut1);
  ntuple1->Draw("Bz:z >> bz",cut1);

  ntuple1->Draw("By:x >> by_x",cut1);

  c1->Divide(3,2);
  c1->cd(1);
  bx->Draw();

  c1->cd(2);
  by->Draw();

  c1->cd(3);
  bz->Draw();

  c1->cd(5);
  by_x->Draw();


  /*
  TLine l1(0,-4,0,4);
  l1->SetLineStyle(2);
  l1->SetLineWidth(2);
  l1->Draw();

  */

  c1.SaveAs("Q1_magnetic_field.png");
  cout << "Number of muons: " <<   bz->GetEntries() << endl; 




}
 
