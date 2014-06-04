# -*- encoding : utf-8 -*-
class UsersController < ApplicationController
  before_filter :only_admin

  def resend_invitation
    @user = User.find(params[:id])
    @user.invite!(current_user)
    render "devise/invitations/create"
  end

  def destroy
    @user = User.find(params[:id])
    if @user.destroy
      flash[:notice] = "Usunięto użytkownika"
    else
      flash[:error] = "Nie udało się usunąć użytkownika."
    end
    redirect_to new_user_invitation_path
  end
end