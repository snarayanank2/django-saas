import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { WorkspacesListComponent } from './workspaces-list/workspaces-list.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { SigninFormComponent } from './signin-form/signin-form.component';

@NgModule({
  declarations: [
    AppComponent,
    WorkspacesListComponent,
    PageNotFoundComponent,
    SigninFormComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
