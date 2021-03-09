// Fit the DIPOLE measurement and compare the field with the magic spreadsheet one

void fit_field(){

  ////////////////////////
  Int_t max_current = 440;
  Float_t max_field = 1.8;
  ///////////////////////
  
  TCanvas *c1 = new TCanvas("c1", "Dipole field", 1800 , 600);
  c1->Divide(3,1);

  Double_t I,B;
  Double_t x[100];  
  Double_t y[100];  

  string dummy;
  Int_t i = 0;

  ifstream is;
  //  is.open("measurement/d2_center_down.txt");
  //  is.open("measurement/d1_centre_up_first.txt");
  is.open("measurement/d1_average.txt");
  //is.open("measurement/d2_average.txt");

  while (is.good())
    {
      is >> I >> B;
      y[i]=I;
      x[i]=B/1000;

      i++;

    }
  is.close();

  c1->cd(1);

  cout << "New fit I(B): " << endl;
  TGraph* graph = new TGraph(i,x,y);
  graph->GetXaxis()->SetTitle("B [T]");
  graph->GetYaxis()->SetTitle("Current [A]");
  TF1 *func2=new TF1("func2","[0]+[1]*x+[2]*x^2+[3]*x^3",0,max_field);
  graph->Fit("func2");
  //graph->Draw("A*");

  cout << endl << "New fit B(I): " << endl;
  TGraph* graph = new TGraph(i,y,x);
  graph->SetTitle("Field vs current");
  graph->GetXaxis()->SetTitle("Current [A]");
  graph->GetYaxis()->SetTitle("B [T]");
  TF1 *func=new TF1("func","[0]+[1]*x+[2]*x^2+[3]*x^3",0,max_field);
  graph->Fit("func");
  graph->Draw("A*");
  

  // Comparison:
  
  c1->cd(2);
  
  // Magic Spreadsheet
  TF1 *MS=new TF1("MS","[0]+[1]*x+[2]*x^2+[3]*x^3",0,max_field);
  MS->SetParameters(0,253.91,-55.998,39.59);
  MS->SetLineColor(1);  //black
  MS->Draw();

  // Fit
  func2->SetLineColor(2);  //red
  func2->Draw("same");

  // Difference:
  TGraph* difference = new TGraph(max_current);
  
  for (int i=0; i<=max_current; i++){
    if (MS->GetX(i,0,2)!=0) difference->SetPoint(i,i, ( func2->GetX(i,0,2) - MS->GetX(i,0,2))/MS->GetX(i,0,2)*100  );
    // difference->SetPoint(i,i, (MS->GetX(i,0,2)-func->Eval(i))*1000  );
  }
  
  
  c1->cd(3);
  
  difference->SetTitle("MS corrections vs Currents");
  difference->GetXaxis()->SetTitle("Current [A]");
  difference->GetYaxis()->SetTitle("Fit - MagicSpreadsheet[%]");
  
  difference->Draw("A*");
  
  

  ///////////////////////////////////
  
  cout << "Currents: " << endl;
  fit(50);
  fit(100);
  fit(146.5);
  fit(200);
  fit(250);
  fit(300);
  fit(350);
  fit(400);
  fit(440);

  c1->SaveAs("saturation_curve.png");


}
 
void fit(double current) {

  double correction;

  cout << "Magic: I= " << current << "A, B=" << MS->GetX(current,0,2) << endl;
  cout << "Fit:   I= " << current << "A, B=" << func->Eval(current) << endl;

  correction= (func->Eval(current)-MS->GetX(current,0,2))/func->Eval(current);
  cout << correction*100 << "%" << endl;
  cout << "New current: " << current-current*correction << endl << endl;

}

