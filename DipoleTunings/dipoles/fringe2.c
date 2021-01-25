// Ascii to vectors and TGraph

{

 

  Float_t x, y, z, t, Px, Py, Pz, Bx, By, Bz, Ex, Ey, Ez;
  Int_t PDGid, EventID, i, j;
  string dummy;
  
  
  Double_t data_Z[10000];
  Double_t MC_Z[10000];

  Double_t data_B[10000];
  Double_t MC_B[10000];

  i=0;
  j=0;

  ifstream is;
  is.open("measurement/fringe.txt");

  while (is.good())
    {

      is >> z >> By;
      //      data_Z[i] = z - 150 + 1000;      //rescale
      data_Z[i] = 700.46 - 6.7-(750-z) -26.21 + 1000;      //rescale
      data_B[i] = By/1000;
      //      cout << z << " - " << data_B[i]  << endl;
      i++;

    }
  is.close();

  data_Z[i] = 0; 
  data_B[i] = 0;
  i++;
  

  is.open("newD2_field.txt");

  getline(is,dummy);
  getline(is,dummy);
  while (is.good())
    {

      is >> x >> y >> z >> t >> Bx >> By >> Bz >> Ex >> Ey >> Ez;           

      if (x==0 && y==0) {
	MC_Z[j] = z;
	MC_B[j] = By;
	j++;
      }
  
    }
  is.close();


  TCanvas *c1 = new TCanvas("c1", "Dipole D2", 1000, 600);

  TGraph* graph1 = new TGraph(j,MC_Z,MC_B);
  graph1->GetXaxis()->SetRangeUser(0,2000);
  graph1->GetYaxis()->SetRangeUser(0,0.45);
  graph1->GetXaxis()->SetTitle("Rescaled z [mm]");
  graph1->GetYaxis()->SetTitle("B [mT]");
  graph1->SetTitle("On axis field");

  TGraph* graph2 = new TGraph(i,data_Z,data_B);
  graph2->GetXaxis()->SetRangeUser(0,2000);
  graph2->GetYaxis()->SetRangeUser(0,0.45);
  graph2->SetTitle("Measured");

  cout << endl << "Fit data..." << endl;
  TF1 *enge = new TF1("enge","0.42/( 1+exp( [0] + [1]*(x-[6]) + [2]*(x-[6])^2 + [3]*(x-[6])^3  + [4]*(x-[6])^4 + [5]*(x-[6])^5 ))  ",1000,1800);
  enge->SetParameter(6, 1000);      

  graph2->Fit("enge","R");

  cout << endl << "Fit new MC..." << endl;
  TF1 *enge2 = new TF1("enge2","0.42/( 1+exp([0] + [1]*(x-[6]) + [2]*(x-[6])^2 + [3]*(x-[6])^3  + [4]*(x-[6])^4 + [5]*(x-[6])^5 )) ",1000,1800);
  enge2->SetParameter(6, 1000);      
  enge2->SetLineColor(4);

  graph1->Fit("enge2","R");
  
  //  TF1 *tanh = new TF1("tanh","0.42/2*(tanh(([3]*x-[1])/[2])+1)",1000,2000);
  //  graph2->Fit("tanh");

  graph1->Draw("AC");
  graph2->Draw("* same");
  //  enge->Draw("same");

  c1.SaveAs("Field_on_axis.png");

}





 
