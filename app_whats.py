import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp chat analyzer")


upload_file =st.sidebar.file_uploader("Upload any file that you want to analyze ")
if upload_file is not None:
    bytes_data=upload_file.getvalue()
    data=bytes_data.decode("utf-8")
    #st.text(data)
    #st.text("new data let us see")
    df=preprocessor.preprocess(data)
    #st.dataframe(df)

    #fetching unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show analysis with respect to ",user_list)

    if st.sidebar.button("Show analysis  "):

        num_messages,word,num_media_messages,no_of_links=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        c1,c2,c3,c4=st.columns(4)

        with c1:
            st.header("Total Messages ")
            st.title(num_messages)
        with c2:
            st.header("\nTotal words ")
            st.title(word)

        with c3:
            st.header("Total files ")
            st.title(num_media_messages)
        with c4:
            st.header("Total links ")
            st.title(no_of_links)

        #monthly timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'],color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='yellow')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most busy Month")
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='gray')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekely Activity HeatMap")
        activity_hp=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(activity_hp)
        st.pyplot(fig)

        #finding most active user in the group chat
        if selected_user == 'Overall':
            st.title("Most active user")
            x,per_df=helper.most_active_user(df)
            fig,ax=plt.subplots()

            c1, c2 = st.columns(2)
            with c1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with c2:
                st.dataframe(per_df)

        #word cloud
        st.title("Word Cloud")
        df_wc=helper.create_word_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        st.title("Most Common Words")
        most_common_df=helper.most_common_words(selected_user,df)
        #st.dataframe(most_common_df)

        fig,ax=plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #emoji analysis
        st.title("Emoji analysis ")
        emoji_df=helper.emoji_analysis(selected_user,df)
        #st.dataframe(emoji_df)
        isempty = emoji_df.empty
        c1,c2=st.columns(2)


        if isempty == False:
            with c1:
                st.subheader("Emoji's with their name and count ")
                st.dataframe(emoji_df)
            with c2:
                st.subheader("Emoji's Barchart")
                fig, ax = plt.subplots()
                ax.bar(emoji_df['emoji_name'].head(18), emoji_df[1].head(18))
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            st.subheader("Frequently used Emoji's Piechart")
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(6), labels=emoji_df['emoji_name'].head(6))
            # plt.xticks(rotation='vertical')
            st.pyplot(fig)
        else:
            st.subheader("Nothing to show")
