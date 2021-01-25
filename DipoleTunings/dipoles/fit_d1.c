// Fit the D1 measurement and compare the field with the magic spreadsheet one

void fit_d1(double current) {

  Double_t I,B;
  Double_t x[100];  
  Double_t y[100];  

  string dummy;
  Int_t i = 0;

  ifstream is;
  //is.open("measurement/center_down.txt");
  //is.open("measurement/d1_up.txt");
  is.open("measurement/d1_average.txt");
  //is.open("measurement/d1_centre_up_second.txt");
  //is.open("measurement/d1_outside_up.txt");

  while (is.good())
    {
      is >> I >> B;
      y[i]=I;
      x[i]=B;

      i++;

    }
  is.close();

  cout << "New fit: " << endl;
  TGraph* graph = new TGraph(i,x,y);
  graph->Fit("pol3");
  graph->Draw("A*");

  TGraph* graph = new TGraph(i,y,x);
  graph->GetXaxis()->SetTitle("Current [A]");
  graph->GetYaxis()->SetTitle("B [T]");
  graph->SetTitle("D2");
  graph->Fit("pol3");
  graph->Draw("A*");
  c1->SaveAs("B_vs_I.png");

  // Magic Spreadsheet
  TF1 *func1=new TF1("func1","[0]+[1]*x+[2]*x^2+[3]*x^3",0,1.6);
  func1->SetParameters(0,253.91,-55.998,39.59);
  func1->SetLineColor(1);  //black
  func1->Draw();

  // Fit
  TF1 *func2=new TF1("func2","[0]+[1]*x+[2]*x^2+[3]*x^3",0,1.6);
  //func2->SetParameters(-16.4174,337.503,-160.296,78.0383);//d1_outside_up
  func2->SetParameters(-5.47485,287.446,-99.2982,53.6564);//d1_average
  func2->SetLineColor(2);  //red
  func2->Draw("same");

  /*fit(100);
  fit(142.66);
  fit(180.7);
  fit(200);
  fit(210.61);
  fit(240);
  fit(350);
  fit(142.66);  
  fit(153);
  */
  cout << "9883,10243:" << endl;
  fit(146.494995);
  cout << "9885:" << endl;
  fit(153.014999);
  cout << "9886:" << endl;
  fit(173.839996);

  cout << "ok, and higher mom.. emittance = 3 " << endl;
  cout << "170, 9911:" << endl;
  fit(160.820007);
  cout << "200, 9910:" << endl;
  fit(185.25);
  cout << "240, 9909:" << endl;
  fit(210.634995);

  cout << "3,6,10-200:" << endl;
  cout << "9760, 3-200" << endl;
  fit(185.25);
  cout << "9761, 6-200" << endl;
  fit(202.914993);
  cout << "9763, 10-200" << endl;
  fit(214.020004);

  cout << "6,10-240:" << endl;
  cout << "10404, 6-200" << endl;
  fit(230.244995);
  cout << "10405, 10-200" << endl;
  fit(250.039993);
  
  cout << "Input current:" << endl;
  fit(current);

  cout << "B=1T, DeltaI=" << func1(1,0,2)-func2(1,0,2) << endl;
  cout << "B=1T, DeltaI=" << func1(1.1,0,2)-func2(1.1,0,2) << endl;
  cout << "B=1T, DeltaI=" << func1(1.2,0,2)-func2(1.2,0,2) << endl;
  cout << "B=1T, DeltaI=" << func1(1.3,0,2)-func2(1.3,0,2) << endl;

}


void fit(double current) {

  double correction;

  cout << "Magic: I= " << current << "A, B=" << func1->GetX(current,0,2) << endl;
  cout << "Fit:   I= " << current << "A, B=" << func2->GetX(current,0,2) << endl;
  
  correction= (func2->GetX(current,0,2)-func1->GetX(current,0,2))/func2->GetX(current,0,2);
  cout << correction*100 << "%" << endl;
  cout << "New current: " << current-current*correction << endl << endl;

} 
